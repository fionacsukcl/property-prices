from property_prices.scripts import output_price_paid_json as oppj


def test_generate_transactions():
    input_file = "./test_data/test_generate_transactions_input_1.csv"
    output_file = "./test_data/test_generate_transactions_output_1.txt"

    with open(output_file, 'r') as file:
        expected_output = eval(file.read())
    actual_output = oppj.generate_transactions(input_file)
    assert expected_output == actual_output


def test_generate_line_per_property():
    input_file = "./test_data/test_generate_line_per_property_input_1.txt"
    output_file = "./test_data/test_generate_line_per_property_output_1.txt"

    with open(input_file, 'r') as file:
        input_data = eval(file.read())
        actual_output = oppj.generate_line_per_property(input_data)

    with open(output_file, 'r') as file:
        expected_output = eval(file.read())
    assert expected_output == actual_output
