import { Component, OnInit } from '@angular/core';
import { GlobalFilter } from './global-filter.model'
import { GlobalFilterService } from './global-filter.service'
import { SharedService } from '../shared.service';
import { global_filter } from '../app.component'
@Component({
  selector: 'app-global-filter',
  templateUrl: './global-filter.component.html',
  styleUrls: ['./global-filter.component.css']
})
export class GlobalFilterComponent implements OnInit {
  Dropdownitems: GlobalFilter[] = [];
  constructor(private _globalfilter: GlobalFilterService, private _sharedService: SharedService) { }

  ngOnInit() {
    this._globalfilter.getData().subscribe(data => {
      data.forEach(element => {
        this.Dropdownitems.push(element);
      });
    });
  }

  updateDropdown(item) {
    global_filter['country_id'] = item;
    this._sharedService.publishData(null);
    // this._sharedService.publishData(global_filter);
  }

}
