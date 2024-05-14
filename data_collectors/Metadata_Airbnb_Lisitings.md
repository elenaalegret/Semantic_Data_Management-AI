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

### Host Information
- `host_id`: Unique identifier for the host.
- `host_url`: URL of the host's Airbnb profile.
- `host_name`: Name of the host.
- `host_since`: Date when the host joined Airbnb.
- `host_location`: Location of the host.
- `host_about`: Bio of the host.
- `host_response_time`: Average response time of the host.
- `host_response_rate`: The percentage of new messages the host replied to within 24 hours over the last 30 days.
- `host_acceptance_rate`: The percentage of booking requests the host accepted over the last 30 days.
- `host_thumbnail_url`, `host_picture_url`: URLs to the host's profile picture.
- `host_neighbourhood`: Neighbourhood the host lists themselves under.
- `host_listings_count`, `host_total_listings_count`: Number of listings the host has in total.

### Location Details
- `street`, `neighbourhood`, `neighbourhood_cleansed`, `neighbourhood_group_cleansed`, `city`, `state`, `zipcode`, `market`, `smart_location`, `country_code`, `country`: Various attributes detailing the listing's location.
- `latitude`, `longitude`: Geographic coordinates of the listing.
- `geolocation.lon`, `geolocation.lat`: Alternative fields for geographic coordinates.

### Property Details
- `property_type`, `room_type`, `accommodates`, `bathrooms`, `bedrooms`, `beds`, `bed_type`: Details about the property type, room type, and capacity.
- `amenities`: List of amenities provided with the listing.
- `square_feet`: Size of the property.

### Pricing Information
- `price`, `weekly_price`, `monthly_price`, `security_deposit`, `cleaning_fee`, `extra_people`: Pricing details for the listing, including any deposits and fees.

### Stay Details
- `guests_included`, `minimum_nights`, `maximum_nights`, `calendar_updated`, `has_availability`, `availability_30`, `availability_60`, `availability_90`, `availability_365`: Details about booking availability and stay requirements.

### Review Scores
- `number_of_reviews`, `first_review`, `last_review`, `review_scores_rating`, `review_scores_accuracy`, `review_scores_cleanliness`, `review_scores_checkin`, `review_scores_communication`, `review_scores_location`, `review_scores_value`, `reviews_per_month`: Information about the reviews and ratings the listing has received.

### Miscellaneous
- `license`, `jurisdiction_names`, `cancellation_policy`, `calculated_host_listings_count`, `features`: Various other attributes including licensing, jurisdiction, and cancellation policy.


## Usage Notes
This dataset is intended for researchers, analysts, and hobbyists interested in the Airbnb market in Barcelona, specifically focusing on listings. It can be used to perform analyses on pricing strategies, location desirability, room type popularity, and host responsiveness.
