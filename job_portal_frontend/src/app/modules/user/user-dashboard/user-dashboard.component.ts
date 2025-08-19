import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SharedModule } from "../../../shared/shared.module";
import { ContentService, UserDashboardContent } from '../../../core/services/content.service';
import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-user-dashboard',
  imports: [CommonModule, ReactiveFormsModule, SharedModule, RouterModule],
  templateUrl: './user-dashboard.component.html',
  styleUrl: './user-dashboard.component.css'
})
export class UserDashboardComponent implements OnInit {
  searchForm: FormGroup;
  dashboardContent: UserDashboardContent | null = null;
  isLoading = true;

  constructor(
    private fb: FormBuilder, 
    private router: Router,
    private contentService: ContentService,
    private authService: AuthService
  ) {
    this.searchForm = this.fb.group({
      query: [''],
      location: ['']
    });
  }

  ngOnInit(): void {
    this.loadDashboardContent();
  }

  loadDashboardContent(): void {
    this.contentService.getUserDashboardContent().subscribe({
      next: (content) => {
        this.dashboardContent = content;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading dashboard content from service:', error);
        // Set fallback content if service fails
        this.dashboardContent = {
          hero: {
            title: 'Find Your Dream Job',
            subtitle: 'Connect with top employers and discover opportunities',
            searchSuggestions: 'Designer, Programming, Digital Marketing, Video, Animation',
            ctaButtonText: 'Find Job'
          },
          welcome: {
            title: 'Welcome to Job Portal',
            content: 'Create an account or sign in to see jobs that fit your requirements',
            ctaButtonText: 'Get Started',
            secondaryLinks: [
              { url: '/user/user-profile', text: 'Post your resume' },
              { url: '#', text: 'Post a job' }
            ]
          },
          howItWorks: {
            title: 'How Job Portal Works',
            steps: [
              {
                icon: 'fas fa-user-plus',
                title: 'Create account',
                number: 1,
                description: 'Fill in all your details for setting up your profile visible to recruiters.'
              },
              {
                icon: 'fas fa-upload',
                title: 'Upload Resume',
                number: 2,
                description: 'Showcase your skills and experience with a standout CV.'
              },
              {
                icon: 'fas fa-search',
                title: 'Find suitable job',
                number: 3,
                description: 'Use smart filters to discover jobs tailored for you.'
              },
              {
                icon: 'fas fa-paper-plane',
                title: 'Apply Easily',
                number: 4,
                description: 'Send applications in one click and track your progress.'
              }
            ]
          },
          heroImage: {
            url: '/assets/person_searching_job.png',
            alt: 'Person searching job'
          }
        };
        this.isLoading = false;
      }
    });
  }

  onSearch() {
    const { query, location } = this.searchForm.value;
    
    console.log('Search initiated with query:', query, 'location:', location);
    
    // Check if user is logged in to determine which route to use
    const isLoggedIn = this.authService.isLoggedIn();
    const currentUser = this.authService.getCurrentUser();
    
    console.log('User logged in:', isLoggedIn);
    console.log('Current user:', currentUser);
    
    if (isLoggedIn && currentUser) {
      // Authenticated user - go to user job search
      console.log('Navigating to /user/job-search');
      this.router.navigate(['/user/job-search'], {
        queryParams: { 
          q: query || null, 
          l: location || null 
        },
        queryParamsHandling: 'merge'
      });
    } else {
      // Non-authenticated user - go to public job search
      console.log('Navigating to /public/jobs');
      this.router.navigate(['/public/jobs'], {
        queryParams: { 
          q: query || null, 
          l: location || null 
        },
        queryParamsHandling: 'merge'
      });
    }
  }
}