## [Version 1.1.0]()
### Create a new Transient Model, Menuitem, and Views:

- Book Names (Text field): A comma-separated list of book names (e.g., Book1, Book2, Book3).
- Author (Many2one): A required field linking to the res.partner model for selecting an author. This field must be mandatory for creating products.

## [Version 1.2.0]()
### Create Two Buttons

- Create Products:
This button will create new `product.template` records based on the book names provided in the Book Names field.
The button should only create new products that do not already exist, preventing duplicates.


- Revert Changes:
This button will be visible only after products have been created using this Bulk Upload Books Record.
If clicked, it will delete all products created from the current Bulk Upload Books Record session.
It should not be visible if no products have been created yet.

## [Version 1.3.0]()
### Adding Smart Button for Products Count
- [Prod Count] Products: This smart button will display the count of books created from this model.
- It will redirect the user to the list of products created from this Bulk Upload Books Record.
- The button will only be visible if products have been created using this Bulk Upload Books Record.
- If no products are created, the button will not appear. If only one product is created from this Bulk Upload Books Record then this button will redirect the user to the form view of that product.