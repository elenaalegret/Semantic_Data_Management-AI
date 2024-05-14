# TripAdvisor Locations in Barcelona -- Dataset Metadata

## General Information
- **Title**: TripAdvisor Locations in Barcelona
- **Themes**: Travel, Tourism, Geography, Urban planning
- **Description**: This dataset contains information about various locations in Barcelona as listed on TripAdvisor. It includes details such as location ID, names, distances, and addresses, providing a comprehensive view of travel-related spots in the city.
- **Identifier**: `tripadvisor-locations`
- **Source**: [TripAdvisor](https://www.tripadvisor.com/)
- **Data Provided By**: [TripAdvisor API](https://developer-tripadvisor.com/content-api/)
- **Last Modified**: April 24, 2024
- **License**: Usage restricted to educational and non-commercial purposes.

## Dataset Attributes

### Basic Location Information
- `location_id`: Unique identifier for each location listed.
- `name`: Name of the location.
- `distance`: Distance from the apartment from which it was scrapped in kilometers.
- `bearing`: Compass bearing from the reference point to said apartment.
- `type`: Category or type of the location (e.g., restaurant, museum, hotel).
- `district`: District or neighborhood where the location is situated.

### Address Details
- `address_obj.street1`: Primary street address of the location.
- `address_obj.street2`: Secondary street address (if applicable).
- `address_obj.city`: City where the location is found.
- `address_obj.state`: State or region of the location.
- `address_obj.country`: Country of the location.
- `address_obj.postalcode`: Postal code for the location.
- `address_obj.address_string`: Full address string as commonly used.

## Usage Notes
This dataset is designed for use by researchers, planners, marketers, and travel enthusiasts who are interested in analyzing location-based data within Barcelona. It offers insights into the types of destinations available in the area, their geographic distribution, and accessibility.

