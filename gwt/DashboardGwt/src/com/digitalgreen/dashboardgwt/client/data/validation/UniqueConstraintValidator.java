package com.digitalgreen.dashboardgwt.client.data.validation;

import java.util.ArrayList;

import com.digitalgreen.dashboardgwt.client.data.BaseData;
import com.google.gwt.gears.client.database.DatabaseException;
import com.google.gwt.user.client.Window;

public class UniqueConstraintValidator extends BaseValidator {
	private BaseData baseData = null;
	private String checkId = null;
	
	public UniqueConstraintValidator(ArrayList value, BaseData baseData) {
		super(value);
		this.baseData = baseData;
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
			query += (String)whereClausePart.get(0) + "='" + (String)whereClausePart.get(1) + "'"; 
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
			return false;
		}
		BaseData.dbClose();
		return true;
	}
}