import { Component, OnInit } from '@angular/core';
import { GlobalFilter } from './global-filter.model'
import { GlobalFilterService } from './global-filter.service'
import { SharedService } from '../shared.service';
import { global_filter } from '../app.component';
import { GlobalFilterSharedService } from '../global-filter/global-filter-shared.service';
@Component({
  selector: 'app-global-filter',
  templateUrl: './global-filter.component.html',
  styleUrls: ['./global-filter.component.css']
})
export class GlobalFilterComponent implements OnInit {
  Dropdownitems: GlobalFilter[] = [];
  constructor(private _globalfilter: GlobalFilterService, private _sharedService: SharedService,
    private _globalfiltersharedService: GlobalFilterSharedService) { }
  country: string = '';

  ngOnInit() {
    this._globalfilter.getData().subscribe(data => {
      data.forEach(element => {
        this.Dropdownitems.push(element);

        if ('country_id' in global_filter) {
          if (element.id == global_filter['country_id']) {
            this.country = element.value;
          }
        } else {
          this.country = this.Dropdownitems[0].value;
        }
      });
    });
  }

  updateDropdown(item) {
    this.country = item.value;
    console.log(item);
    global_filter[item.tagName] = item.id;
    // TODO : if Dropdown level more than 2 => handling
    if (item.parentTag) {
      global_filter[item.parentTag] = item.parentId;
    }
    console.log(global_filter);
    this._globalfiltersharedService.publishData();
    // this._sharedService.publishData(global_filter);
  }

}
