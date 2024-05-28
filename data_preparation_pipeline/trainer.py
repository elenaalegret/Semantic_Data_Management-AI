
# Import
import torch
from torchkge.models import TransEModel
from torchkge.sampling import BernoulliNegativeSampler
from torchkge.utils import DataLoader, MarginLoss
import numpy as np
from tqdm import tqdm

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def train_model(kg_train, kg_val=None, emb_dim=100, n_epochs=1000, b_size=32768, lr=0.0004, margin=0.5):
    """
    Trains an embedding model using torchKGE with a custom training loop.

    :param kg_train: KnowledgeGraph, the training knowledge graph
    :param kg_val: KnowledgeGraph, the validation knowledge graph (optional)
    :param emb_dim: int, the dimension of the embeddings
    :param n_epochs: int, the number of epochs to train
    :param b_size: int, the batch size for training
    :param lr: float, the learning rate
    :param margin: float, the margin value for the TransE loss function
    :return: None
    """
    # Define the embedding model
    model = TransEModel(emb_dim, kg_train.n_ent, kg_train.n_rel, dissimilarity_type='L2')

    # Define the optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    # Define the loss function
    criterion = MarginLoss(margin)

    # Define the negative sampler and dataloader
    sampler = BernoulliNegativeSampler(kg_train)
    dataloader = DataLoader(kg_train, batch_size=b_size, use_cuda='')

    # Training loop
    iterator = tqdm(range(n_epochs), unit='epoch')
    for epoch in iterator:
        model.train()
        running_loss = 0.0
        for i, batch in enumerate(dataloader):
            h, t, r = batch[0], batch[1], batch[2]
            n_h, n_t = sampler.corrupt_batch(h, t, r)

            optimizer.zero_grad()

            # Forward + backward + optimize
            pos, neg = model(h, t, r, n_h, n_t)
            loss = criterion(pos, neg)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        iterator.set_description(
            'Epoch {} | mean loss: {:.5f}'.format(epoch + 1, running_loss / len(dataloader)))

        # Validation
        if kg_val is not None:
            model.eval()
            val_loss = 0.0
            val_loader = DataLoader(kg_val, batch_size=b_size, use_cuda='all')
            for i, batch in enumerate(val_loader):
                h, t, r = batch[0], batch[1], batch[2]
                n_h, n_t = sampler.corrupt_batch(h, t, r)

                with torch.no_grad():
                    pos, neg = model(h, t, r, n_h, n_t)
                    loss = criterion(pos, neg)
                    val_loss += loss.item()
            print('Validation loss: {:.5f}'.format(val_loss / len(val_loader)))

        # Normalize model parameters
        model.normalize_parameters()

    # Obtain the embeddings
    entity_embeddings = model.ent_emb.weight.data.cpu().numpy()
    relation_embeddings = model.rel_emb.weight.data.cpu().numpy()

    # Save the embeddings
    np.save('entity_embeddings.npy', entity_embeddings)
    np.save('relation_embeddings.npy', relation_embeddings)

    print(f'Entity embeddings shape: {entity_embeddings.shape}')
    print(f'Relation embeddings shape: {relation_embeddings.shape}')
