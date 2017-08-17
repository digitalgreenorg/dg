import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CardsService } from './cards.service';
import { SharedService } from '../shared.service';
import { environment } from '../../environments/environment.loop';
import { IMyOptions } from 'mydatepicker';
import { DatePipe } from '@angular/common';
import { global_filter } from '../app.component';
import { GlobalFilterSharedService } from '../global-filter/global-filter-shared.service';

@Component({
  selector: 'app-cards',
  templateUrl: './cards.component.html',
  styleUrls: ['./cards.component.css']
})

export class CardsComponent implements OnInit, AfterViewInit {
  cardsOverall = [];
  cardsRecent = [];
  charts = [];
  overallcharts = [];
  recentcharts = [];
  cardGraphConfig = environment.cardGraphConfig;
  Dropdownitems = [];
  recentChartsData = {};
  private chooseDateRange:string = '';

  // DatePicker
  private date = new Date();
  public endModel = {
    date: {
      day: this.date.getDate(),
      month: this.date.getMonth() + 1,
      year: this.date.getFullYear()
    }
  };
  public startModel = {
    date: {
      day: new Date(this.date.setDate(this.date.getDate() + 1)).getDate(),
      month: new Date(this.date.setMonth(this.date.getMonth() + 1)).getMonth(),
      year: new Date(this.date.setFullYear(this.date.getFullYear() - 1)).getFullYear()
    }
  };

  private myDatePickerOptions: IMyOptions = {
    dateFormat: 'dd-mm-yyyy',
    alignSelectorRight: true,
    showClearDateBtn: false,
    // editableDateField: false,
    indicateInvalidDate: true,
    inline: false,
    maxYear: this.date.getFullYear() + 1,
    selectionTxtFontSize: '16px',
  };

  constructor(private cardsService: CardsService, private _sharedService: SharedService, private datepipe: DatePipe
  , private _globalfiltersharedService:GlobalFilterSharedService) {
        this._globalfiltersharedService.argsList$.subscribe(data => {
          let options = this.createParams();
          this.getData(options);
        });
  }
  cardsConfigs = environment.cardsConfig;

  ngOnInit(): void {
    Object.keys(this.cardsConfigs).forEach(key => {
      if (this.cardsConfigs[key].overall.cards) {
        this.cardsOverall.push({
          'id': key,
          'text': this.cardsConfigs[key].text
        });
      } else if (this.cardsConfigs[key].overall.graph) {
        this.overallcharts.push({
          tagName: this.cardsConfigs[key].overall.text,
          title: this.cardsConfigs[key].text,
          options: this.cardsConfigs[key].overall.graph.options,
          nativeChart: null,
        });
      }

      if (this.cardsConfigs[key].recent.cards) {
        this.cardsRecent.push({
          'id': key,
          'text': this.cardsConfigs[key].text
        });
      }
      else if (this.cardsConfigs[key].recent.graph) {
        this.recentcharts.push({
          tagName: this.cardsConfigs[key].recent.text,
          title: this.cardsConfigs[key].text,
          options: this.cardsConfigs[key].recent.graph.options,
          nativeChart: null,
        });
      }
    });
    // let options = {
    //   webUrl: "getData/",
    //   params: {
    //     apply_filter: false,
    //   }
    // }
    // Uncomment for filter Request
    // this.getData(options);

  }

  ngAfterViewInit(): void {
    let options = this.createParams();
    this.getData(options);
  }

  public getData(options): any {
    Object.keys(this.cardsConfigs).forEach(key => {
      if (this.cardsConfigs[key].overall.borrowData == false) {
        options.params.cardName = this.cardsConfigs[key].overall.text;
        this.saveData(options);
      }
      if (this.cardsConfigs[key].recent.borrowData == false) {
        options.params.cardName = this.cardsConfigs[key].recent.text;
        this.saveData(options);
      }
    });
  }

  saveInstance(chartInstance, chart) {
    chart.nativeChart = chartInstance;
  }

  public saveData(options): any {
    this.cardsService.getApiData(options)
      .subscribe(dataList => {
        dataList['data'].forEach(cardData => {
          if (cardData.placeHolder == "overall") {
            this.cardsOverall.forEach(card => {
              if (card.text == cardData.tagName) {
                card['value'] = cardData.value;
              }
            });
          }
          if (cardData.placeHolder == "recent") {
            this.cardsRecent.forEach(card => {
              if (card.text == cardData.tagName) {
                card['value'] = cardData.value;
              }
            });
          }
          if (cardData.placeHolder == "overallcardGraphs") {
            this.overallcharts.forEach(chart => {
              if (cardData.tagName === chart.tagName) {
                chart.nativeChart.series[0].update({ 'data': [cardData.value] });
              }
            });
          }
          if (cardData.placeHolder == "recentcardGraphs") {
            this.recentcharts.forEach(chart => {
              if (cardData.tagName === chart.tagName) {
                this.Dropdownitems = Object.keys(cardData.value);
                this.recentChartsData[cardData.tagName] = cardData.value;
                chart.nativeChart.series[0].update({ 'data': cardData.value['15'] });
              }
            })
            this.chooseDateRange = '15' + ' Days';
          }
        });
      });
  }

  public updateDropdown(day): any {
    this.chooseDateRange = day + ' Days';
    this.recentcharts.forEach(chart => {
      chart.nativeChart.series[0].update({ 'data': this.recentChartsData[chart.tagName][day] });
    });
  }

  private createParams() : any {
    let options = {
      webUrl: "getCardGraphData/",
      params: {
        apply_filter: false,
      }
    };
    Object.assign(options.params, global_filter);
    return options;
  }
}
