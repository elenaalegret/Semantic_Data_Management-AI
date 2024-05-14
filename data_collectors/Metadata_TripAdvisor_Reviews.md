# TripAdvisor Reviews in Barcelona -- Dataset Metadata

## General Information
- **Title**: TripAdvisor Reviews in Barcelona
- **Themes**: Travel, Consumer reviews, Tourism analysis
- **Description**: This dataset comprises reviews of various locations in Barcelona as published on TripAdvisor. It includes detailed attributes such as review ID, language, ratings, subratings, and user information, providing insights into user experiences and opinions.
- **Identifier**: `tripadvisor-reviews-barcelona`
- **Source**: [TripAdvisor](https://www.tripadvisor.com/)
- **Data Provided By**: [TripAdvisor API](https://developer-tripadvisor.com/content-api/)
- **Last Modified**: April 24, 2024
- **License**: Usage restricted to educational and non-commercial purposes.

## Dataset Attributes

### Review Details
- `id`: Unique identifier for each review.
- `lang`: Language of the review.
- `location_id`: Identifier linking the review to a specific location.
- `published_date`: Date when the review was published.
- `rating`: Overall rating given by the user.
- `helpful_votes`: Number of users who found the review helpful.
- `rating_image_url`: URL to an image representing the rating.
- `url`: URL to the full review on TripAdvisor.
- `text`: Full text of the review.
- `title`: Title of the review.
- `trip_type`: Type of trip reported in the review (e.g., business, leisure).
- `travel_date`: Date of travel as reported by the reviewer.

### User Information
- `user.username`: Username of the reviewer.
- `user.user_location.id`: Unique identifier for the reviewer's location.
- `user.user_location.name`: Name of the reviewer's location.
- `user.avatar.thumbnail`: URL to the thumbnail size of the user's avatar.
- `user.avatar.small`: URL to the small size of the user's avatar.
- `user.avatar.medium`: URL to the medium size of the user's avatar.
- `user.avatar.large`: URL to the large size of the user's avatar.
- `user.avatar.original`: URL to the original size of the user's avatar.

### Subratings
- `subratings.x.name`: Name of the subrating category (x indicates multiple subratings are possible).
- `subratings.x.rating_image_url`: URL to an image representing the subrating.
- `subratings.x.value`: Numeric value of the subrating.
- `subratings.x.localized_name`: Localized name of the subrating category.

### Owner Response
- `owner_response.id`: Unique identifier for the owner's response.
- `owner_response.title`: Title of the owner's response.
- `owner_response.text`: Text of the owner's response.
- `owner_response.lang`: Language of the owner's response.
- `owner_response.author`: Author of the owner's response.
- `owner_response.published_date`: Date when the owner's response was published.

## Usage Notes
This dataset is valuable for researchers and analysts looking to study consumer behavior, satisfaction, and feedback regarding tourism locations in Barcelona. It offers a deep dive into detailed reviews and can be used for sentiment analysis, trend identification, and quality assessment in the travel and tourism industry.

