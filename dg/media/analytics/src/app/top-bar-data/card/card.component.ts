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
export class CardComponent {
  @Input() cardId: String;
  @Input() cardData: Overall[];
  constructor() {}
}
