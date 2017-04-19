import { Component, OnInit } from '@angular/core';
import { TopBarDataService } from '../top-bar-data.service';
import { MyData} from '../my-data';
import { STAT } from '../config/config-data'
@Component({
  selector: 'app-top-bar-data',
  templateUrl: './top-bar-data.component.html',
  styleUrls: ['./top-bar-data.component.css'],
})

export class TopBarDataComponent implements OnInit {

  private myData : MyData[];
  private myData1 : MyData[];
  title;
  val;
  private webUrl = 'http://localhost:8000/training/testmethod/'
  constructor(
    private topbardataService : TopBarDataService
  ) {
  }

  getOverAllData(webUrl) : void {
    // console.log(STAT[0].overall.apiUrl)
    this.topbardataService.getData(webUrl)
                          .subscribe(val => this.myData = val);
  }
  
  getRecentData(webUrl) : void {
    // console.log(STAT[0].overall.apiUrl)
    this.topbardataService.getData(webUrl)
                          .subscribe(val => this.myData1 = val);
  }
  
  // To get values of cards parameter
  getCardsData(stat) : void {
    
  }
  showData() : void{
    console.log(this.myData);
  }

  ngOnInit() {
    for(let stat of STAT) {
      if(stat.overall.show) {
        this.getOverAllData(stat.overall.apiUrl);
      }
      if(stat.recent.show) {
        this.getRecentData(stat.overall.apiUrl);
      }
      
    }
    
    this.showData();
  }

}
