import { Component, OnInit } from '@angular/core';
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

export class TopBarDataComponent implements OnInit {
  cardDataDict: { [id: string]: Overall[] } = {};
  configData: Overall;
  val;

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
        /*start_date: this.datepipe.transform(this.startModel.date.year.toString() + '-' + this.startModel.date.month.toString() + '-' + this.startModel.date.day.toString(), 'yyyy-MM-dd'),
        end_date: this.datepipe.transform(this.endModel.date.year.toString() + '-' + this.endModel.date.month.toString() + '-' + this.endModel.date.day.toString(), 'yyyy-MM-dd'),
        */
        apply_filter: false,
      }
    }
    this.getDatatest(options);
  }

}
