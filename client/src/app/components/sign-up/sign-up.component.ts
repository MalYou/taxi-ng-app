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

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  onSubmit(f: NgForm): void {
    if(f.valid) {
      this.authService.signUp(
        f.controls['userName'].value,
        f.controls['firstName'].value,
        f.controls['lastName'].value,
        f.controls['password'].value,
        f.controls['group'].value,
        f.controls['photo'].value,
      ).subscribe(() => {
        this.router.navigateByUrl('/log-in');
      }, (error) => {
        console.error(error);
      });
    }
  }
}