import { Component,OnInit, AfterViewInit } from '@angular/core';
import { CardsService } from './cards.service';
import { SharedService } from '../shared.service';
import { cardConfigs } from './configs';

@Component({
    selector: 'app-cards',
    templateUrl: './cards.component.html',
    styleUrls: ['./cards.component.css']
})

export class CardsComponent implements OnInit {
    cardsOverall = [];
    cardsRecent = [];
    
    constructor(private cardsService: CardsService, private sharedService: SharedService) {
        this.sharedService.argsList$.subscribe(data => {
        this.getData(data);
      });
    }

    ngOnInit(): void {
        Object.keys(cardConfigs).forEach(key => {
            if(cardConfigs[key].overall.show){
                this.cardsOverall.push({
                    'id': key,
                    'text':cardConfigs[key].text
                });
            }
            if(cardConfigs[key].recent.show){
                this.cardsRecent.push({
                    'id':key,
                    'text':cardConfigs[key].text
                });
            }
        })
        let options = {
            webUrl: 'http://localhost:8000/training/getData',
            params: {
              apply_filter: false,
            }
        }
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
                  else {
                      this.cardsRecent.forEach(card => {
                        if(cardData.tagName === card.text){
                          card['value'] = cardData.value;
                        }
                      });
                  }         
              });
          });
    }
}

