import {
  Component,
  OnInit,
  Input,
  OnChanges,
  SimpleChanges,
  ElementRef,
  ViewChild } from '@angular/core';
import { Overall } from '../../config/overall'

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent implements
  OnInit,
  OnChanges {
  @Input() cardId: String;
  @ViewChild('cardTitle') cardTitle: ElementRef;
  @Input() cardData: Overall[];
  constructor() { }

  ngOnInit() {

    // this.cardTitle.nativeElement.id = 'this-test';
    // console.log(this.cardTitle.nativeElement.id);
  }

  showId(id1: any) {
    console.log(id1);
  }
  ngOnChanges(changes: SimpleChanges) {
    // console.log('ngonchanges called');
    // console.log(changes);
  }

}
