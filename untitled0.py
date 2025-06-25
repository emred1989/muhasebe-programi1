# -*- coding: utf-8 -*-
"""untitled0.py 
Ön Muhasebe Mantığı: Cari hesap ve işlemler"""
import pandas as pd
from datetime import datetime

class CurrentAccountManager:
    def __init__(self, filename="current_accounts.csv"):
        self.filename = filename
        try:
            self.accounts = pd.read_csv(self.filename)
            # Kolon kontrolleri ve tip dönüşümleri
            for col, default in [
                ('account_id', None), ('account_name', ''),
                ('account_type', 'Customer'), ('balance', 0.0),
                ('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ]:
                if col not in self.accounts.columns:
                    self.accounts[col] = default
            self.accounts['balance'] = self.accounts['balance'].astype(float)
            self.accounts['created_at'] = pd.to_datetime(self.accounts['created_at'])
        except FileNotFoundError:
            # Yeni boş DataFrame
            self.accounts = pd.DataFrame(columns=[
                'account_id','account_name','account_type','balance','created_at'
            ])
            self.accounts['balance'] = self.accounts['balance'].astype(float)
            self.accounts['created_at'] = pd.to_datetime(self.accounts['created_at'])
        # Transactions
        self.transactions_filename = "transactions.csv"
        try:
            self.transactions = pd.read_csv(self.transactions_filename)
            for col, default in [
                ('transaction_id', None), ('account_id', 0),
                ('transaction_type', 'Credit'), ('amount', 0.0),
                ('description', ''), ('transaction_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ]:
                if col not in self.transactions.columns:
                    self.transactions[col] = default
            self.transactions['account_id'] = self.transactions['account_id'].astype(int)
            self.transactions['amount'] = self.transactions['amount'].astype(float)
            self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
        except FileNotFoundError:
            self.transactions = pd.DataFrame(columns=[
                'transaction_id','account_id','transaction_type','amount','description','transaction_date'
            ])
            self.transactions['account_id'] = self.transactions['account_id'].astype(int)
            self.transactions['amount'] = self.transactions['amount'].astype(float)
            self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])

    def _save_data(self):
        self.accounts.to_csv(self.filename, index=False)
        self.transactions.to_csv(self.transactions_filename, index=False)

    def create_account(self, account_name, account_type="Customer"):
        if account_name in self.accounts['account_name'].values:
            print(f"'{account_name}' zaten var.")
            return None
        next_id = self.accounts['account_id'].max() + 1 if not self.accounts.empty else 1
        new = {
            'account_id': next_id,
            'account_name': account_name,
            'account_type': account_type,
            'balance': 0.0,
            'created_at': datetime.now()
        }
        self.accounts = pd.concat([self.accounts, pd.DataFrame([new])], ignore_index=True)
        self._save_data()
        return next_id

    def list_accounts(self):
        return self.accounts.copy()

    def record_transaction(self, account_id, amount, transaction_type, description=""):
        idx = self.accounts[self.accounts['account_id']==account_id].index
        if idx.empty:
            return False
        if transaction_type.lower()=='credit':
            self.accounts.loc[idx, 'balance'] += amount
        else:
            self.accounts.loc[idx, 'balance'] -= amount
        next_tid = self.transactions['transaction_id'].max()+1 if not self.transactions.empty else 1
        trx = {
            'transaction_id': next_tid,
            'account_id': account_id,
            'transaction_type': transaction_type.capitalize(),
            'amount': amount,
            'description': description,
            'transaction_date': datetime.now()
        }
        self.transactions = pd.concat([self.transactions, pd.DataFrame([trx])], ignore_index=True)
        self._save_data()
        return True

    def get_account_transactions(self, account_id):
        df = self.transactions[self.transactions['account_id']==account_id].copy()
        df['transaction_date'] = df['transaction_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        return df

    def get_receivables(self):
        return self.accounts[self.accounts['balance']>0]

    def get_payables(self):
        df = self.accounts[self.accounts['balance']<0'].copy()
        df['balance'] = df['balance'].abs()
        return df

    def get_account_by_id(self, account_id):
        df = self.accounts[self.accounts['account_id']==account_id]
        return df.iloc[0] if not df.empty else None

    def generate_summary_report(self):
        total_recv = self.get_receivables()['balance'].sum()
        total_pay = self.get_payables()['balance'].sum()
        report = f"Toplam Alacak: {total_recv:.2f}\nToplam Borç: {total_pay:.2f}\n"
        return report
