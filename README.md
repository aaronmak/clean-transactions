# Clean Transactions

Scripts to clean DBS Bank's CSV files

- Bank Transactions
  - Simple download of CSV
- Card Transactions
  - Bank doesn't have CSV output so copy from web into a CSV file


Examples

```python
python clean_bank_transactions.py test/fake-bank-transactions.csv
python clean_card_transactions.py test/fake-card-transactions.csv
```

Should work on most python versions, but to be safe use the one in `.tool-versions` with asdf
