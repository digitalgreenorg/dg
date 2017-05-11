import {
    Component,
    OnInit,
    OnChanges,
    SimpleChanges } from '@angular/core';
import { TopBarDataService } from '../top-bar-data.service';
import { STAT } from '../config/config-data'
import { Config } from '../config/config';
import { Data } from '../config/data';
import { Overall } from '../config/overall';
import { IMyOptions } from 'mydatepicker';
import { DatePipe } from '@angular/common';

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
  private argstest;
  private webUrl = 'http://localhost:8000/training/testmethod/'
  constructor(
    private topbardataService : TopBarDataService,
    private datepipe : DatePipe,
  ) {
  }

  getDatatest(apply_filter) : any {
    this.argstest = {
      webUrl: 'http://localhost:8000/training/getData',
      params: {
        start_date:this.datepipe.transform(this.startModel.date.day.toString() + '-' + this.startModel.date.month.toString() + '-' + this.startModel.date.year.toString(), 'yyyy-MM-dd'),
        end_date:this.datepipe.transform(this.endModel.date.month.toString() + '-' + this.endModel.date.day.toString() + '-' + this.endModel.date.year.toString(), 'yyyy-MM-dd'),
        apply_filter:apply_filter,
      }
    }

    this.topbardataService.getApiData(this.argstest)
                          .subscribe(val => {
                                              console.log(val);
                                              for( let v in val.data) {
                                                let vobj = val.data[v]
                                                for( let d of this.cardDataDict[vobj['placeHolder']]) {
                                                  if(d.tagName == vobj['tagName']) {
                                                    d.value = vobj['value']
                                                  }
                                                }
                                              }
                                            });
  }

  ngOnChanges(changes : SimpleChanges) {
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
    this.getDatatest(false);
  }

}
