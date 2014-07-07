import xlrd
import csv
import os

def csv_from_excel(docfile):
	try:
		wb = xlrd.open_workbook(docfile)
		sh = wb.sheet_by_name('Sheet1')
		docfile = open(docfile+'.csv', 'wb')
		wr = csv.writer(docfile, quoting=csv.QUOTE_ALL)
		for rownum in xrange(sh.nrows):
			wr.writerow(sh.row_values(rownum))
		docfile.close()
		#os.remove('Book1.xlsx')
		print your_csv_file
	except Exception, err:
		print err

	return docfile


def main():
	csv_from_excel(docfile)


if __name__ == '__main__':
	main()
