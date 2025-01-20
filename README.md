# WP-CLI Create Menu Items from Product Categories

## Description
This script generates a navigation structure for WordPress menus (compatible with Max Mega Menu) using WooCommerce product categories. It simplifies menu management by automating the creation, update, and deletion of menu items based on the product category hierarchy.

## Features
- Dynamically create menu items from WooCommerce product categories.
- Support for custom parent items (e.g., grouping specific categories under a parent like "Other").
- Automatically sort items by product count.
- Options to update, delete, or clean up menu items.

## Requirements
- Python 3.6 or later.
- WP-CLI installed and properly configured.
- WooCommerce plugin active in your WordPress installation.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/AllWorkNoPlay-95/wp-cli-create-menu-items-from-prod-cat.git
   cd wp-cli-create-menu-items-from-prod-cat
   ```
2. Ensure the script is executable:
   ```bash
   chmod +x create-menu-items.py
   ```
3. Run the script with the required options.

## Usage
Run the script with the following options:

### Arguments
- `-u, --update-existing`: Update existing menu items by setting parents and order.
- `--delete-all`: Delete all menu items and start fresh.
- `--delete-orphans`: Remove menu items not present in the product categories.
- `-C, --with-count`: Append product counts to the last-level menu items.
- `-v`: Enable verbose mode for detailed output.

### Examples
- Create a new menu structure from product categories:
  ```bash
  ./create-menu-items.py
  ```
- Update an existing menu structure:
  ```bash
  ./create-menu-items.py -u
  ```
- Delete all existing menu items and create a new structure:
  ```bash
  ./create-menu-items.py --delete-all
  ```

## Customization
You can configure:
- Custom parent items by modifying the `custom_parents` variable in the script.
- Categories to exclude by editing `categorySlugsToSkip`.

## License
This script is licensed under the GPL-3.0 License.  
See the [LICENSE](LICENSE) file for more details.

## Author
Developed by **Samuele Mancuso**  
GitHub: [AllWorkNoPlay-95](https://github.com/AllWorkNoPlay-95)

---

## For Recruiters
This project demonstrates proficiency in the following technical areas:

- **Python Programming**: Writing clean, modular, and reusable code for task automation and data processing.
- **WordPress Development**: Integrating with WP-CLI to interact programmatically with WordPress and WooCommerce.
- **JSON Parsing and Manipulation**: Extracting, transforming, and utilizing structured data from various sources.
- **Command Line Automation**: Executing and processing system commands efficiently for dynamic menu generation.
- **Data Structures and Algorithms**: Creating hierarchical structures and sorting algorithms to map complex relationships like nested product categories.
- **Error Handling and Debugging**: Implementing robust error-handling mechanisms to manage cache misses and inconsistencies.
- **Optimization and Scalability**: Designing the script to handle large datasets and multiple levels of hierarchy while maintaining performance.
