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
import { SharedService } from '../shared.service';

@Component({
  selector: 'app-top-bar-data',
  templateUrl: './top-bar-data.component.html',
  styleUrls: ['./top-bar-data.component.css'],
})

export class TopBarDataComponent implements
  OnInit,
  OnChanges {

  cardDataDict: { [id: string]: Overall[] } = {};
  configData: Overall;
  val;
  // DatePicker
  private myDatePickerOptions: IMyOptions = {
    dateFormat: 'dd-mm-yyyy',
  };
  private date = new Date();
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
  private argstest;
  private webUrl = 'http://localhost:8000/training/testmethod/'
  constructor(
    private topbardataService: TopBarDataService,
    private datepipe: DatePipe,
    private _sharedService: SharedService
  ) {
    this._sharedService.argsList$.subscribe(data => {
      this.getDatatest(data);
    });
  }

  public getDatatest(options): any {
    this.topbardataService.getApiData(options)
      .subscribe(val => {
        // console.log(val);
        for (let v in val.data) {
          let vobj = val.data[v]
          for (let d of this.cardDataDict[vobj['placeHolder']]) {
            if (d.tagName == vobj['tagName']) {
              d.value = vobj['value'];
            }
          }
        }
      });
  }

  ngOnChanges(changes: SimpleChanges) {
  }

  ngOnInit() {
    for (let stat of STAT) {
      for (let configItems in stat) {
        this.configData = new Overall();
        if (stat[configItems].show) {
          this.configData.tagName = stat.entity_name;
          this.configData.placeHolder = stat[configItems].placeHolder;
          this.configData.value = null;
          if (!(stat[configItems].placeHolder in this.cardDataDict)) {
            this.cardDataDict[stat[configItems].placeHolder] = []
          }
          this.cardDataDict[stat[configItems].placeHolder].push(this.configData);
        }
      }
    }

    let options = {
      webUrl: 'http://localhost:8000/training/getData',
      params: {
        start_date: this.datepipe.transform(this.startModel.date.year.toString() + '-' + this.startModel.date.month.toString() + '-' + this.startModel.date.day.toString(), 'yyyy-MM-dd'),
        end_date: this.datepipe.transform(this.endModel.date.year.toString() + '-' + this.endModel.date.month.toString() + '-' + this.endModel.date.day.toString(), 'yyyy-MM-dd'),
        apply_filter: false,
      }
    }
    this.getDatatest(options);
  }

}
