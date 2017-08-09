import { Component, OnInit } from '@angular/core';
import { GlobalFilter } from './global-filter.model'
import { GlobalFilterService } from './global-filter.service'

@Component({
  selector: 'app-global-filter',
  templateUrl: './global-filter.component.html',
  styleUrls: ['./global-filter.component.css']
})
export class GlobalFilterComponent implements OnInit {
  Dropdownitems : GlobalFilter[] = [];
  constructor(private _globalfilter:GlobalFilterService) { }

  ngOnInit() {
    // this.Dropdownitems.push({name:'India', id:1, isSelected:true});
    // this.Dropdownitems.push({name:'Bangladesh', id:2, isSelected:false});
    this._globalfilter.getData().subscribe(data => {
      data.forEach(element => {
        this.Dropdownitems.push(element);
      });
      console.log(this.Dropdownitems);
    });
  }

  updateDropdown(item) {
    console.log(item);
  }

}
