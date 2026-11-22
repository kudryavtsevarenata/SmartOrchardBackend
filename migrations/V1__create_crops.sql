CREATE TABLE crops (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name varchar(60) NOT NULL,
    variety varchar(60),
    row_spacing numeric NOT NULL CHECK (row_spacing > 0),
    tree_spacing numeric NOT NULL CHECK (tree_spacing > 0),
    prefix text NOT NULL
);
