package com.digitalgreen.dashboardgwt.client.data.validation;

import java.util.ArrayList;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class UniqueConstraintValidator extends BaseValidator {
	protected BaseData baseData = null;
	protected String checkId = null;
	protected ArrayList labels;
	
	public UniqueConstraintValidator(ArrayList labels, ArrayList value, BaseData baseData ) {
		super(value);
		this.baseData = baseData;
		this.labels = labels;
	}

	public void setCheckId(String checkId) {
		this.checkId = checkId;
	}
	
	@Override
	public boolean validate() {
		BaseData.dbOpen();
		String query = "SELECT * FROM " + this.baseData.getTableName() + " WHERE ";
		ArrayList whereClause = ((ArrayList)this.getValue());
		// For composite unique indexes
		for(int i=0; i < whereClause.size(); i++) {
			ArrayList whereClausePart = (ArrayList)whereClause.get(i);
			if((String)whereClausePart.get(1) != null) {
				query += (String)whereClausePart.get(0) + "='" + ((String)whereClausePart.get(1)).trim() + "' COLLATE NOCASE";
			} else {
				query += "("+(String)whereClausePart.get(0) + " is null" +" OR "+ (String)whereClausePart.get(0) + " = \"\" )" ;
			}
			if(i != whereClause.size() - 1) {
					query += " AND ";
			}
		}
		query += ";";
		this.baseData.select(query);
		if (this.baseData.getResultSet().isValidRow()) {
			try {
				if(this.checkId != null && 
						this.baseData.getResultSet().getFieldAsString(0).equals(this.checkId)) {
					BaseData.dbClose();
					return true;
				}
			} catch (DatabaseException e) {
				e.printStackTrace();
			} finally {
				BaseData.dbClose();
			}
			ArrayList childLabels = (ArrayList)this.labels;
			for(int i=0; i < childLabels.size(); i++) {
				errorString += childLabels.get(i)+", ";
			}
			errorString += uniqueValidatorErrorMessage;
			return false;
		}
		BaseData.dbClose();
		return true;
	}
}