import { Component, OnInit } from '@angular/core';
import { GetDataFromServerService } from '.././get-data-from-server/get-data-from-server.service';

@Component({
  selector: 'app-analytics-table',
  templateUrl: './analytics-table.component.html',
  styleUrls: ['./analytics-table.component.css']
})
export class AnalyticsTableComponent implements OnInit {

  data: JSON;
  errorMessage: string;
  responseData: string = "Not Updated";
  constructor(private getTableData:GetDataFromServerService) { }

  ngOnInit(): void {
    this.getTableData.getData().subscribe((data:JSON) => {
      this.data = data;
      console.log("From Component : ");
      console.log(data);
      this.responseData = "Updated";
    },
  error => {this.errorMessage = <any>error, this.responseData=this.errorMessage});
  }

}
