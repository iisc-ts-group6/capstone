import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-side-nav',
  templateUrl: './side-nav.component.html',
  styleUrl: './side-nav.component.css'
})
export class SideNavComponent {
  //isExpanded = true;
  showSubmenu: boolean = false;
  isShowing = true;
  showSubSubMenu: boolean = false;
  selectedMenu: string = "dashboard";
  @ViewChild('sidenav') sidenav!: MatSidenav;
  currentUrl: string;
  email!: string;
  constructor(private router: Router) {
    this.currentUrl = '';
  }

  ngOnInit(): void {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.currentUrl = event.urlAfterRedirects;
        console.log(this.currentUrl)
        if (typeof window !== 'undefined') { // Check if window is defined
          this.email = localStorage.getItem("email") ?? '';
        }
      }
    });
  }

  signOut(){
    localStorage.clear();
    this.router.navigateByUrl('/auth/sign-in');
  }

  // mouseenter() {
  //   if (!this.isExpanded) {
  //     this.isShowing = true;
  //   }
  // }

  // mouseleave() {
  //   if (!this.isExpanded) {
  //     this.isShowing = false;
  //   }
  // }

  menuSelected(menuName: string) {
    this.selectedMenu = menuName;

  }
}
