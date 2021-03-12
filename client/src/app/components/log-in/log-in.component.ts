import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';

class UserData {
  constructor(
    public username?: string,
    public password?: string
  ) {}
}

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent {
  user: UserData = new UserData();
  constructor(
    private router: Router,
    private authService: AuthService
  ) {}
  onSubmit(f: NgForm): void {
    if(f.valid) {
      this.authService.logIn(
        f.controls['username'].value, f.controls['password'].value
      ).subscribe(user => {
        this.router.navigateByUrl('');
      }, (error) => {
        console.error(error);
      });
    }
  }
}