import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';


import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent {
  userPhoto: any;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  onChange(event: any): void {
    if (event.target.files && event.target.files.length > 0) {
      this.userPhoto = event.target.files[0];
    }
  }

  onSubmit(f: NgForm): void {
    if(true) {
      console.log(f);
      this.authService.signUp(
        f.controls['userName'].value,
        f.controls['firstName'].value,
        f.controls['lastName'].value,
        f.controls['password'].value,
        f.controls['group'].value,
        this.userPhoto,
      ).subscribe(() => {
        this.router.navigateByUrl('/log-in');
      }, (error) => {
        console.error(error);
      });
    }
  }
}