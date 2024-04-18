import csv
import hashlib
import ndjson

COLUMNS = {
    0: 'id',
    1: 'price',
    2: 'date_of_transfer',
    3: 'postcode',
    4: 'property_type',
    5: 'old_new',
    6: 'duration',
    7: 'paon',
    8: 'saon',
    9: 'street',
    10: 'locality',
    11: 'town_city',
    12: 'district',
    13: 'country',
    14: 'ppd_category_type',
    15: 'record_status'
}


def main(filename: str) -> None:
    """
    The main function which calls the functions to process the input data.
    Then outputs the results in a multi-line JSON.

    :param filename: The name of the input file.
    """
    transactions_object = generate_transactions(filename)
    output_object = generate_line_per_property(transactions_object)

    with open('../output/output_data.json', 'w') as f:
        ndjson.dump(output_object, f)


def generate_transactions(filename: str) -> dict:
    """
    This function takes a filename as input. A property hash is
    generated for each transaction using the property address, and each column
    in the file is labelled using the COLUMNS dictionary. Also set any empty
    column values to NULL.

    :param filename: The name of the input file.
    :return: A dictionary of transactions with the property hash as
    the key.
    """
    transactions = {}

    with open(filename) as f:
        for row in csv.reader(f):
            # Create a property ID by combining the address fields, separated
            # by a pipe to handle any null values
            property_id = "|".join(
                [
                    row[3],  # Postcode
                    row[7],  # PAON
                    row[8],  # SAON
                    row[9],  # Street
                    row[10],  # Locality
                    row[11],  # Town/City
                    row[12],  # District
                    row[13]  # Country
                 ]
            )
            property_hash = hashlib.sha256(property_id.encode()).hexdigest()
            transaction_data = {}

            # Assign column name to each value in row
            # Set any empty string to NULL
            for index, value in enumerate(row):
                transaction_data[COLUMNS[index]] = (
                    value if value != '' else None)

            # Add transaction and group for transactions with the same address
            if not transactions.get(property_hash):
                transactions[property_hash] = []
            transactions[property_hash].append(transaction_data)
    return transactions


def generate_line_per_property(transactions: dict) -> list:
    """
    Generates a list of dictionary, where each dictionary represents
    a single property with a list of transactions.

    :param transactions: A dictionary of the processed transactions.
    :return: A list of properties and its transactions.
    """
    output_object = []
    for key, value in transactions.items():
        output_object.append({key: value})
    return output_object


if __name__ == "__main__":
    input_file = "../data/price-paid-data.csv"
    main(input_file)
