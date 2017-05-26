import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Filter } from './filter';
import { FilterElement } from './filter-element';
import { GetFilterDataService } from '../get-filter-data.service';
import { SharedService } from '../shared.service';
import { IMyOptions } from 'mydatepicker';
import { DatePipe } from '@angular/common';


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
  private showDateFilter: boolean = false;
  private f_list = {};
  private limit;
  private myDatePickerOptions: IMyOptions = {
    dateFormat: 'dd-mm-yyyy',
    alignSelectorRight: true
  };
  private date = new Date();
  public startModel = {
    date: {
      year: this.date.getFullYear()-1,
      month: this.date.getMonth()+1,
      day: this.date.getDate()+1
    }
  };
  public endModel = {
    date: {
      year: this.date.getFullYear(),
      month: this.date.getMonth()+1,
      day: this.date.getDate()
    }
  };

  constructor(private myElement: ElementRef, private getFilterData: GetFilterDataService, private _sharedService: SharedService, private datepipe: DatePipe) {
    this.limit = 20;
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
        return data.id;
      });
      if (list.length > 0) {
        this.f_list[f.heading] = list;
      }
      this.f_list['apply_filter'] = "true";
    }
    this.f_list['start_date'] = this.datepipe.transform(this.startModel.date.year.toString() + '-' + this.startModel.date.month.toString() + '-' + this.startModel.date.day.toString(), 'yyyy-MM-dd');
    this.f_list['end_date'] = this.datepipe.transform(this.endModel.date.year.toString() + '-' + this.endModel.date.month.toString() + '-' + this.endModel.date.day.toString(), 'yyyy-MM-dd');
    this.getDatatest();
  }

  getDatatest(): any {
    let argstest = {
      webUrl: 'http://localhost:8000/training/getData',
      params: this.f_list
    }
    this._sharedService.publishData(argstest);
  }

  handleClick(event) {
    let clickedComponent = event.target;
    let inside = false;
    do {
      if (clickedComponent === this.myElement.nativeElement) {
        inside = true;
      }
      clickedComponent = clickedComponent.parentNode;
    } while (clickedComponent);

    if (inside) {
    } else {
      this.closeNav();
    }
  }
}
