import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { FILTER_DATA } from './filter-data';
import { Filter } from './filter';
import { FilterElement } from './filter-element';
import { GetFilterDataService } from '../get-filter-data.service';
import { TopBarDataService } from '../top-bar-data.service';
import { SharedService } from '../shared.service';
// import { TopBarDataComponent } from '../top-bar-data/top-bar-data.component';


@Component({
  selector: 'app-filters',
  host: {
    '(document:click)': 'handleClick($event)',
  },
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.css']
})
export class FiltersComponent implements OnInit {

  @ViewChild('mySidenav') mySidenav: ElementRef;
  filter_list: Filter[] = new Array<Filter>();
  filter: Filter;
  private showDateFilter: boolean;
  private f_list = {};
  constructor(private myElement: ElementRef, private getFilterData: GetFilterDataService,private _sharedService: SharedService) {
  }

  ngOnInit() {

    this.getFilterData.getData().subscribe(val => {
      for (let data of val) {
        if (data['name'] === 'date' && data['visible'] == true) {
          this.showDateFilter = true;
        }
        else {
          this.filter = new Filter();
          this.filter.heading = data['name'];
          this.filter.expand = false;
          this.filter.element = new Array<FilterElement>();
          for (let val of data['data']) {
            let filterElement = new FilterElement();
            filterElement.id = val['id'];
            filterElement.value = val['value'];
            filterElement.checked = false;

            this.filter.element.push(filterElement);
          }
          this.filter_list.push(this.filter);
        }
      }
    });
  }

  closeNav() {
    this.mySidenav.nativeElement.style.width = '0px';
  }

  openNav() {
    this.mySidenav.nativeElement.style.width = '320px';
  }

  applyFilters() {
    this.f_list = {};
    for (let f of this.filter_list) {
      let list = f.element.filter(data => { return data.checked }).map(data => {
        return data.id
      });
      this.f_list[f.heading] = list;
    }
    this.f_list['apply_filter'] = "true";
    this.getDatatest();
  }

  getDatatest(): any {
    let argstest = {
      webUrl: 'http://localhost:8000/training/getData',
      params: this.f_list
    }
    this._sharedService.publishData(argstest);
    // this.topbardataService.getApiData(argstest)
    //   .subscribe(val => {
    //     console.log(val);
    //   });
    // this.topBarDataComponent.getDatatest(argstest);

  }

  handleClick(event) {
    var clickedComponent = event.target;
    var inside = false;
    do {
      if (clickedComponent === this.myElement.nativeElement) {
        inside = true;
      }
      clickedComponent = clickedComponent.parentNode;
    } while (clickedComponent);

    if (inside) {
      // this.closeNav();
      // console.log('inside');
    } else {
      // console.log('outside');
      this.closeNav();
    }
  }

}
