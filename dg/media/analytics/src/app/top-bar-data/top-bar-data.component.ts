import { Component, OnInit } from '@angular/core';
import { TopBarDataService } from '../top-bar-data.service';
import { MyData} from '../my-data';
import { STAT } from '../config/config-data'
import { Config } from '../config/config';
import { Data } from '../config/data'
import { Overall } from '../config/overall'
import { IMyOptions } from 'mydatepicker'
import { DatePipe } from '@angular/common'

@Component({
  selector: 'app-top-bar-data',
  templateUrl: './top-bar-data.component.html',
  styleUrls: ['./top-bar-data.component.css'],
})

export class TopBarDataComponent implements OnInit {

  private myData : MyData[];
  private myData1 : MyData[];
  private myApiData:Config[] = new Array<Config>();
  // private myApiData:Config = new Config();
  private testConfig: Config = new Config();
  private testApidata: Config = new Config();
  private data: Data = new Data();
  title;
  val;
  private testdate;
  
  // DatePicker
  private myDatePickerOptions: IMyOptions = {
    dateFormat : 'dd-mm-yyyy',
  };
  private date = new Date();
  public disabled:boolean = false;
  private start_date = new Date(2015, 1, 1);
  public startModel = {
                                  date: { 
                                    year: this.start_date.getFullYear(),
                                    month: this.start_date.getMonth(),
                                    day: this.start_date.getDate()
                                  }
                                };
  public endModel = {
                                date: { 
                                    year: this.date.getFullYear(),
                                    month: this.date.getMonth(),
                                    day: this.date.getDate()
                                  }
                              };
  
  // End Datepicker
  private args;
  private webUrl = 'http://localhost:8000/training/testmethod/'
  constructor(
    private topbardataService : TopBarDataService,
    private datepipe : DatePipe,
  ) {
  }
  
  // To get ApiResult in the class format
  getData(stat) : void {
    this.args = {
      webUrl: stat.apiUrl,
      params: {
        start_date:this.datepipe.transform(this.startModel.date.day.toString() + '-' + this.startModel.date.month.toString() + '-' + this.startModel.date.year.toString(), 'yyyy-MM-dd'),
        end_date:this.datepipe.transform(this.endModel.date.month.toString() + '-' + this.endModel.date.day.toString() + '-' + this.endModel.date.year.toString(), 'yyyy-MM-dd'),
      }
    }
    
    this.topbardataService.getApiData(this.args)
                          .subscribe(val => {this.myApiData.push(val); console.log('data -> ', val)})
  }
  showData() : void {
    
    this.data.overall = new Overall();
    this.data.overall.tagName = 'sujit'
    this.data.overall.value = 123
    // console.log('sd -> ', this.testdate.getDate());
    // this.testConfig.data = {
    //   overall: [{
    //   tagName:'sujit',
    //   value:10
    //   }],
    //   recent:[{
    //     tagName:'chandru',
    //     value: 20
    //   }]
    // };
    // this.testOverall = {
    //   tagName:'aman',
    //   value:30
    // }
    // this.testConfig.data.overall.push(this.testOverall);
    // console.log(this.testConfig.data.overall[0].tagName);
  }
  
  public getfilteredData():any {
    this.myApiData = new Array<Config>();
    for(let stat of STAT) {
        
      // api call
      if(stat.graphs.show) {
        this.getData(stat);
      }
    }
  }

  ngOnInit() {

    for(let stat of STAT) {

      // api call
      if(stat.graphs.show) {
        this.getData(stat);
      }
    }
    this.showData();
    
  }



}
