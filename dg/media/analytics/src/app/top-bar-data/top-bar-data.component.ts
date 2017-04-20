import { Component, OnInit } from '@angular/core';
import { TopBarDataService } from '../top-bar-data.service';
import { MyData} from '../my-data';
import { STAT } from '../config/config-data'
import { Config } from '../config/config';

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
  
  title;
  val;
  private testOverall;
  
  
  private webUrl = 'http://localhost:8000/training/testmethod/'
  constructor(
    private topbardataService : TopBarDataService
  ) {
  }

  getOverAllData(webUrl) : void {
    // console.log(STAT[0].overall.apiUrl)
    this.topbardataService.getData(webUrl)
                          .subscribe(val => {this.myData = val;});
  }
  
  getRecentData(webUrl) : void {
    // console.log(STAT[0].overall.apiUrl)
    this.topbardataService.getData(webUrl)
                          .subscribe(val => this.myData1 = val);
  }
  
  // To get ApiResult in the class format
  getData(stat) : void {
    this.topbardataService.getApiData(stat.apiUrl)
                          .subscribe(val => {this.myApiData.push(val); console.log('data -> ', val)})
  }
  showData() : void {
    
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

  ngOnInit() {

    for(let stat of STAT) {
      if(stat.overall.show) {
        this.getOverAllData(stat.overall.apiUrl);
      }
      if(stat.recent.show) {
        this.getRecentData(stat.overall.apiUrl);
      }

      // api call
      if(stat.graphs.show) {
        this.getData(stat);
      }
    }
    this.showData();
  }

}
