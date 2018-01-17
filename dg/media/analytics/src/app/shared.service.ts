import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';

@Injectable()
export class SharedService {
  // Observable argument list source
  private argsList = new Subject<any>();
  // Observable argument streams
  argsList$ = this.argsList.asObservable();

  // Service message commands
  public publishData(data: any) {
    this.argsList.next(data);
  }
}
