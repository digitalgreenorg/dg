import { 
    Component, 
    OnInit,
    OnChanges,
    SimpleChanges } from '@angular/core';
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

export class TopBarDataComponent implements 
  OnInit,
  OnChanges {

  private myApiData:Config[] = new Array<Config>();
  private testConfig: Config = new Config();
  overAllData:Overall[] = new Array<Overall>();
  recentData:Overall[] = new Array<Overall>();
  cardDataDict: {[id:string] : Overall[]} = {};
  configData:Overall;
  val;
  overalltest:Overall = new Overall();
  recentTest:Overall = new Overall();
  overallobj:Overall = new Overall();
  private testdate;
  private reload = true;
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
                          .subscribe(val => {
                                              for(let v in val.data) {
                                                for(let d in this.cardDataDict[v]) {
                                                  let o = this.cardDataDict[v][d]
                                                  if(this.reload && o.placeHolder == 'overallBar') {
                                                    if(o.tagName == val.data[v].tagName) {
                                                        o.value = val.data[v].value;
                                                    }
                                                  } else {
                                                    if(o.tagName == val.data[v].tagName && o.placeHolder != 'overallBar') {
                                                      o.value = val.data[v].value;
                                                    }
                                                  }
                                                } 
                                              }
                                            })
  }
  
  getfilteredData():any {
    this.reload = false;
    for(let stat of STAT) {
      // api call
      if(stat.overall.show) {
        this.getData(stat);
      }
    }
  }
  
  ngOnChanges(changes : SimpleChanges) {
    console.log('onChanges called TopBarDataComponent');
    console.log(changes);
  }

  ngOnInit() {
    for (let stat of STAT) {
      for (let configItems in stat) {
        this.configData = new Overall();
        if(stat[configItems].show) {
          this.configData.tagName = stat.entity_name;
          this.configData.placeHolder = stat[configItems].placeHolder;
          this.configData.value = null;
          if(!(stat[configItems].placeHolder in this.cardDataDict)) {
            this.cardDataDict[stat[configItems].placeHolder] = []
          }
          this.cardDataDict[stat[configItems].placeHolder].push(this.configData);
        }
      }
    }
    console.log(this.cardDataDict);
    for(let stat of STAT) {
      // api call
      if(stat.overall.show) {
        this.getData(stat);
      }
    }
  }

}
