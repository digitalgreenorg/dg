import { Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { TopBarDataService } from '../top-bar-data.service';
import { IMyOptions } from 'mydatepicker';
import { SharedService } from '../shared.service';

@Component({
  selector: 'app-cards',
  templateUrl: './cards.component.html',
  styleUrls: ['./cards.component.css']
})
export class CardsComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
