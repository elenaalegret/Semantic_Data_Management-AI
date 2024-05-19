# Airbnb Listings in Barcelona -- Dataset Metadata

## General Information
- **Title**: Airbnb Listings in Barcelona
- **Themes**: Spatial planning, Town planning, Buildings, Equipment, Housing
- **Description**: This dataset comprises Airbnb listings in Barcelona, Spain. It includes a variety of attributes for each listing, such as the type of room, the number of listings per host, verification methods, amenities, and other features specific to each listing.
- **Identifier**: `airbnb-listings`
- **Source**: [OpenDataSoft](https://public.opendatasoft.com/explore/dataset/airbnb-listings/information/?disjunctive.host_verifications&disjunctive.amenities&disjunctive.features&q=barcelona&refine.city=Barcelona)
- **Data Provided By**: [Inside Airbnb](http://insideairbnb.com/get-the-data.html)
- **Last Modified**: February 22, 2024 3:42 PM
- **License**: CC 0 1.0

## Dataset Attributes

### Listing Information
- `id`: Unique identifier for each listing.
- `listing_url`: URL of the listing on Airbnb.
- `scrape_id`: Unique identifier for the scrape session.
- `last_scraped`: Date when the listing was last scraped.
- `name`: Name of the listing.
- `summary`: Brief summary of the listing.
- `space`: Description of the space provided by the host.
- `description`: Full description of the listing.
- `experiences_offered`: Type of experiences offered with the listing.
- `neighborhood_overview`: Host's description of the neighborhood.
- `notes`: Additional notes provided by the host.
- `transit`: Information on local transit options.
- `access`: Details about what parts of the property guests can access.
- `interaction`: Host's preferences about interacting with guests.
- `house_rules`: Rules set by the host for guests.

### Photos URLs
- `thumbnail_url`, `medium_url`, `picture_url`, `xl_picture_url`: URLs to various sizes of the listing's main photo.

### Location Details
- `latitude`, `longitude`: Geographic coordinates of the listing.

### Property Details
- `property_type`, `room_type`, `accommodates`, `bathrooms`, `bedrooms`, `beds`, `bed_type`: Details about the property type, room type, and capacity.

### Pricing Information
- `price`, `weekly_price`, `monthly_price`, `security_deposit`, `cleaning_fee`, `extra_people`: Pricing details for the listing, including any deposits and fees.

### Stay Details
-  `minimum_nights`, `maximum_nights`, `calendar_updated`, `has_availability`, `availability_30`, `availability_60`, `availability_90`, `availability_365`: Details about booking availability and stay requirements.

### Review Scores
- `number_of_reviews`, `review_scores_rating`, `review_scores_value`: Information about the reviews and ratings the listing has received.

## Usage Notes
This dataset is intended for researchers, analysts, and hobbyists interested in the Airbnb market in Barcelona, specifically focusing on listings. It can be used to perform analyses on pricing strategies, location desirability, room type popularity, and host responsiveness.
