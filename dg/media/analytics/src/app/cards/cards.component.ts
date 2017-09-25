import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CardsService } from './cards.service';
import { SharedService } from '../shared.service';
import { global_filter } from '../app.component';
import { GlobalFilterSharedService } from '../global-filter/global-filter-shared.service';
import { CardsGraph } from './cardsgraph.model'
import { Cards } from './cards.model';
import { environment } from '../../environments/environment.training';

@Component({
  selector: 'app-cards',
  templateUrl: './cards.component.html',
  styleUrls: ['./cards.component.css']
})

export class CardsComponent implements OnInit, AfterViewInit {

  overallcharts = [];
  recentcharts = [];
  Dropdownitems = [];
  cardsOverall = [];
  cardsRecent = [];

  private charts = [];
  private recentChartsData = {};
  private chooseDateRange: string = '';
  private cardGraphConfig = environment.cardGraphConfig;
  private cardsConfigs = environment.cardsConfig;

  constructor(private cardsService: CardsService, private _sharedService: SharedService
    , private _globalfiltersharedService: GlobalFilterSharedService) {
    this._globalfiltersharedService.argsList$.subscribe(data => {
      let options = this.createParams();
      this.getCardsData(options);
    });
  }

  ngOnInit(): void {
    Object.keys(this.cardsConfigs).forEach(key => {
      if (this.cardsConfigs[key].overall.cards) {
        this.initCards(this.cardsOverall, key);
      } else if (this.cardsConfigs[key].overall.graph) {
        this.initCardsGraph(this.overallcharts, key, 'overall');
      }

      if (this.cardsConfigs[key].recent.cards) {
        this.initCards(this.cardsRecent, key);
      }
      else if (this.cardsConfigs[key].recent.graph) {
        this.initCardsGraph(this.recentcharts, key, 'recent');
      }
    });
  }

  initCards(cards, key) : void {
    let cardsobj : Cards = {
      'id': key,
      'text': this.cardsConfigs[key].text
    }
    cards.push(cardsobj);
  }

  initCardsGraph(cards, data, option) : void {

    let cardsgraphobj = {} as CardsGraph;
    cardsgraphobj.title = this.cardsConfigs[data].text;
    cardsgraphobj.nativeChart = null;
    cardsgraphobj.lastDataPoint = 0;

    if(option == 'overall') {
      cardsgraphobj.tagName = this.cardsConfigs[data].overall.text;
      cardsgraphobj.options = this.cardsConfigs[data].overall.graph.options;
      cardsgraphobj.helpTip = this.cardsConfigs[data].helpTip;

    } else if(option == 'recent') {
      cardsgraphobj.tagName = this.cardsConfigs[data].recent.text;
      cardsgraphobj.options = this.cardsConfigs[data].recent.graph.options;
      cardsgraphobj.helpTip = '';
    }

    cards.push(cardsgraphobj)

  }

  ngAfterViewInit(): void {
    this.showLoadingMessage();
    let options = this.createParams();
    this.getCardsData(options);
  }

  showLoadingMessage(): void {
    this.recentcharts.forEach(chart => {
      chart.nativeChart.showLoading();
    });
  }

  public getCardsData(options): any {
    Object.keys(this.cardsConfigs).forEach(key => {
      if (this.cardsConfigs[key].overall.borrowData == false) {
        options.params.cardName = this.cardsConfigs[key].overall.text;
        this.fetchData(options);
      }
      if (this.cardsConfigs[key].recent.borrowData == false) {
        options.params.cardName = this.cardsConfigs[key].recent.text;
        this.fetchData(options);
      }
    });
  }

  saveInstance(chartInstance, chart) {
    chart.nativeChart = chartInstance;
  }

  public fetchData(options): any {
    this.cardsService.getApiData(options)
      .subscribe(dataList => {
        console.log(dataList['data'])
        dataList['data'].forEach(cardData => {
          if (cardData.placeHolder == "overall") {
            this.cardsOverall.forEach(card => {
              if (card.text == cardData.tagName) {
                card['value'] = cardData.value;
              }
            });
          }
          else if (cardData.placeHolder == "recent") {
            this.cardsRecent.forEach(card => {
              if (card.text == cardData.tagName) {
                card['value'] = cardData.value;
              }
            });
          }
          else if (cardData.placeHolder == "overallcardGraphs") {
            this.overallcharts.forEach(chart => {
              if (cardData.tagName === chart.tagName) {
                chart.nativeChart.series[0].update({ 'data': [cardData.value] });
              }
            });
          }
          else if (cardData.placeHolder == "recentcardGraphs") {
            let numberOfDays = Object.keys(cardData.value)[0];
            let dataToDisplay = cardData.value[numberOfDays];
            this.recentcharts.forEach(chart => {
              if (cardData.tagName === chart.tagName) {
                chart.lastDataPoint = dataToDisplay[dataToDisplay.length - 1];
                this.Dropdownitems = Object.keys(cardData.value);
                this.recentChartsData[cardData.tagName] = cardData.value;
                chart.nativeChart.series[0].update({ 'data': dataToDisplay, 'name': cardData.tagName });
                if (dataToDisplay.length > 0) {
                  chart.nativeChart.hideLoading();
                } else {
                  chart.nativeChart.showLoading("No data found");
                }
              }
            });
            this.chooseDateRange = numberOfDays + ' Days';
          }
        });
      });
  }

  public updateDropdown(day): any {
    this.chooseDateRange = day + ' Days';
    this.recentcharts.forEach(chart => {
      let dataToDisplay = this.recentChartsData[chart.tagName][day];
      chart.lastDataPoint = dataToDisplay[dataToDisplay.length - 1];
      chart.nativeChart.series[0].update({ 'data': dataToDisplay });
    });
  }

  private createParams(): any {
    let options = {
      params: {
        apply_filter: false,
      }
    };
    Object.assign(options.params, global_filter);
    return options;
  }
}
