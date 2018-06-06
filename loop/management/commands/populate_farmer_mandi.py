import os
import sys
from django.core.management.base import BaseCommand, CommandError
from loop.models import *
from django.db.models import Count,Min,Sum

class Command(BaseCommand):
    help = '''This command updates stats displayed on Loop dashboard. '''

    def handle(self,*args,**options):
        print("Log")
        print("LOOP FARMER MANDI LOG")
        print(datetime.date.today())
        populate = Populate()
        populate.updateFarmerJoiningData()
        populate.updateFarmerMandiData()

        populate.updateFarmerMandiData()
        populate.updateFarmerTransactionData()
        #populate.updateFarmerJoiningData()

class Populate():
	def updateFarmerMandiData(self):
		farmerTransactions = CombinedTransaction.objects.values('farmer','mandi').annotate(transaction_count=Count('date',distinct=True)).distinct()
		for transactionObject in farmerTransactions:
			farmerMandi = FarmerMandi(farmer_id=transactionObject['farmer'],mandi_id=transactionObject['mandi'],transaction_count=transactionObject['transaction_count'])
			farmerMandi.save()

	def updateFarmerJoiningData(self):
		farmers = Farmer.objects.filter(date_of_joining=None)
		farmerTransactions = CombinedTransaction.objects.filter(farmer__in=farmers,farmer__date_of_joining=None).values('farmer').annotate(date_of_joining=Min('date'))
		for transactionObject in farmerTransactions:
			farmer =farmers.get(id=transactionObject['farmer'])
			farmer.date_of_joining = transactionObject['date_of_joining']
			farmer.save()


	def updateFarmerTransactionData(self):
		farmers = Farmer.objects.filter(transaction_count=0)
		farmerTransactions = CombinedTransaction.objects.filter(farmer__in=farmers).values('farmer').annotate(transaction_count=Count('date',distinct=True))
		for transactionObject in farmerTransactions:
			farmer =farmers.get(id=transactionObject['farmer'])
			farmer.transaction_count = transactionObject['transaction_count']
			farmer.save()		

	def updateFarmerVolumeData(self):
		farmers = Farmer.objects.filter(volume=0)
		farmerTransactions = CombinedTransaction.objects.filter(farmer__in=farmers).values('farmer').annotate(volume=Sum('quantity',distinct=True))
		for transactionObject in farmerTransactions:
			farmer =farmers.get(id=transactionObject['farmer'])
			farmer.volume = transactionObject['volume']
			farmer.save()	