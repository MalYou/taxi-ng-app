import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Trip, TripService } from 'src/app/services/trip.service';


@Component({
  selector: 'app-rider-dashboard',
  templateUrl: './rider-dashboard.component.html',
  styleUrls: ['./rider-dashboard.component.css']
})

export class RiderDashboardComponent implements OnInit {
  trips: Trip[] = [];

  constructor(private route: ActivatedRoute, private tripService: TripService) { }

  get currentTrips(): Trip[] {
    return this.trips.filter(trip => {
      return trip.driver !== null && trip.status !== 'COMPLETED';
    });
  }

  get completedTrips(): Trip[] {
    return this.trips.filter(trip => {
      return trip.status === 'COMPLETED';
    });
  }

  ngOnInit(): void {
    this.route.data
      .subscribe((data) => this.trips = data.trips);
  }
}
