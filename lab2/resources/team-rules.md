## Development Rules

### Important

- Schema design should follow star-schema
- Explicit measures enforced for all aggregatable numeric columns, and base column should be hidden
- [Naming conventions](#naming-conventions) should be respected

### Nice to have

- Model shall include an `About` table that describes the Author and version of the model. See [About](#about-table) for details of how to create the table if not exists.

## Appendix

### Naming Conventions

- Business-friendly names, don't use terms as 'Fact' or 'Dim', use plural names for fact tables and singular names for dimension tables (e.g. `Sales`, `Product`, `Customer`). 
- Measures should use readable names in UPPERCASE

### About table

- Create the table with columns:
  - Key: Text
  - Value: Text
  - Order: Number
- Use the following partition configuration:  
  - mode: Import
  - partition source type: m
  - M expression source:
        ```powerquery
        let
            Source = #table({ "Key", "Value" },{
                { "Developed by", "Company X" },
                { "Version", "1.0" },
                { "Description", "[Model Description]" },
                { "Last Refresh", DateTime.ToText(DateTime.LocalNow(), "yyyy-MM-dd HH:mm:ss") }
            }),
            #"Added Index" = Table.AddIndexColumn(Source, "Order", 1, 1),
            #"Changed Type" = Table.TransformColumnTypes(#"Added Index",{{"Key", type text},  {"Value", type text},{"Order", Int64.Type}}),
            #"Reordered Columns" = Table.ReorderColumns(#"Changed Type",{"Key", "Value", "Order"})
        in
            #"Reordered Columns"
        ```