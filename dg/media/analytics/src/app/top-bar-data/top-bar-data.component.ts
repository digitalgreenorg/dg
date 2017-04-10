import { Component, OnInit } from '@angular/core';
import { TopBarDataService } from '../top-bar-data.service';
import { MyData} from '../my-data'

@Component({
  selector: 'app-top-bar-data',
  templateUrl: './top-bar-data.component.html',
  styleUrls: ['./top-bar-data.component.css']
})
export class TopBarDataComponent implements OnInit {

  private myData : MyData[];
  title;
  val;
  
  constructor(
    private topbardataService : TopBarDataService
  ) {
  }

  getData() : void {
    this.topbardataService.getData()
                          .then(val => this.myData = val);
    // .then(val => {this.myData = [
    //         {id : 1, name : 'Sujit'},
    //         {id : 2, name : 'Chandru'}
    //     ]; console.log(this.myData)});
  }

  showData() : void{
    console.log(this.myData);
  }

  ngOnInit() {
    this.getData();
    this.showData();
  }

}
