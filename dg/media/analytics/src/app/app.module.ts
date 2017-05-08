import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { TopBarDataComponent } from './top-bar-data/top-bar-data.component';
import { TopBarDataService } from './top-bar-data.service';
import { AccordionModule } from '../../node_modules/ngx-bootstrap';
import { KeysPipe } from './keys.pipe';
import { GraphComponent } from './graph/graph.component';
import { NvD3Module } from '../../node_modules/angular2-nvd3';
import { MyDatePickerModule } from 'mydatepicker';
import { ButtonsModule } from 'ngx-bootstrap';
import { DatePipe } from '@angular/common';
import { CardComponent } from './top-bar-data/card/card.component';

@NgModule({
  declarations: [
    AppComponent,
    TopBarDataComponent,
    KeysPipe,
    GraphComponent,
    CardComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AccordionModule.forRoot(),
    NvD3Module,
    MyDatePickerModule,
    ButtonsModule.forRoot(),
  ],
  providers: [TopBarDataService, DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
