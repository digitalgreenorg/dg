import { Component,OnInit, AfterViewInit } from '@angular/core';
import { CardsService } from './cards.service';
import { SharedService } from '../shared.service';
import { environment } from '../../environments/environment.loop';

@Component({
    selector: 'app-cards',
    templateUrl: './cards.component.html',
    styleUrls: ['./cards.component.css']
})

export class CardsComponent implements OnInit, AfterViewInit {
    cardsOverall = [];
    cardsRecent = [];
    charts = [];
    cardGraphConfig = environment.cardGraphConfig;
    constructor(private cardsService: CardsService, private sharedService: SharedService) {
        this.sharedService.argsList$.subscribe(data => {
        this.getData(data);
      });
    }
    cardsConfigs = environment.cardsConfig;
    ngOnInit(): void {
        Object.keys(this.cardsConfigs).forEach(key => {
            if(this.cardsConfigs[key].overall.show){
                this.cardsOverall.push({
                    'id': key,
                    'text':this.cardsConfigs[key].text
                });
            }
            if(this.cardsConfigs[key].recent.show){
                this.cardsRecent.push({
                    'id':key,
                    'text':this.cardsConfigs[key].text
                });
            }
        })
        let options = {
            webUrl: "getData",
            params: {
              apply_filter: false,
            }
        }
        this.getData(options);
        // graph-Cards
        Object.keys(this.cardGraphConfig).forEach(config => {
            this.charts.push({
                options:this.cardGraphConfig[config],
                nativeChart:null,
            })
        });
        Object.keys(this.cardsConfigs).forEach(cardData => {
            console.log(this.cardsConfigs[cardData]);
        });
    }

    ngAfterViewInit(): void {
        let options = {
            webUrl : "getCardGraphData",
            params: {
              apply_filter: false,
            }
        };
        this.getData(options);
    }

    public getData(options): any {
        this.cardsService.getApiData(options)
          .subscribe(dataList => {
              dataList['data'].forEach(cardData => {
                  if(cardData.placeHolder == "overall") {
                      this.cardsOverall.forEach(card => {
                        if(cardData.tagName === card.text){
                          card['value'] = cardData.value;
                        }
                      });
                  }
                  else if(cardData.placeHolder == "recent") {
                      this.cardsRecent.forEach(card => {
                        if(cardData.tagName === card.text){
                          card['value'] = cardData.value;
                        }
                      });
                  }
                  else if(cardData.placeHolder == "cardGraphs") {
                    this.charts.forEach(chart=> {
                       chart.nativeChart.series[0].update({'data':[cardData.value]})
                    })
                  }
              });
          });
    }

    saveInstance(chartInstance, chart) {
        chart.nativeChart = chartInstance;
    }
}

