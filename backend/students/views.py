from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Avg, Count
from .models import Student, Department
from .serializers import StudentSerializer, DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Department CRUD operations (SOP Section 7.3 & 7.6).
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for complete Student CRUD operations (SOP Section 7.6 & 8).
    Supports:
      - Create: POST /api/students/
      - Read All: GET /api/students/?search=...&department=...&status=...
      - Read One: GET /api/students/{id}/
      - Update: PUT /api/students/{id}/ or PATCH /api/students/{id}/
      - Delete: DELETE /api/students/{id}/
      - Statistics: GET /api/students/stats/
    """
    queryset = Student.objects.select_related('department').all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        """
        Support search and filtering across records (SOP Section 7.1 & 7.4).
        """
        queryset = super().get_queryset()
        
        # Search by student_id, first_name, last_name, or email
        search_query = self.request.query_params.get('search', None)
        if search_query:
            query = search_query.strip()
            queryset = queryset.filter(
                Q(student_id__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )

        # Filter by department ID
        dept_id = self.request.query_params.get('department', None)
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)

        # Filter by status (Active, Inactive, Graduated, Suspended)
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status__iexact=status_filter)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new student record (SOP Section 7.6 & 8).
        HTTP POST /api/students/
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': 'Validation failed. Please correct the highlighted errors.',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        student = serializer.save()
        return Response(
            {
                'status': 'success',
                'message': f"Student '{student.full_name}' created successfully.",
                'data': StudentSerializer(student).data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """
        Update an existing student record (SOP Section 7.6 & 8).
        HTTP PUT /api/students/{id}/
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': 'Validation failed. Please correct the highlighted errors.',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        student = serializer.save()
        return Response(
            {
                'status': 'success',
                'message': f"Student '{student.full_name}' updated successfully.",
                'data': StudentSerializer(student).data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a student record (SOP Section 7.6 & 8).
        HTTP DELETE /api/students/{id}/
        """
        instance = self.get_object()
        name = instance.full_name
        instance.delete()
        return Response(
            {
                'status': 'success',
                'message': f"Student '{name}' has been deleted."
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Summary metrics for dashboard display.
        HTTP GET /api/students/stats/
        """
        total = Student.objects.count()
        active = Student.objects.filter(status='Active').count()
        avg_gpa = Student.objects.aggregate(avg=Avg('gpa'))['avg'] or 0.00
        by_dept = (
            Student.objects.values('department__name', 'department__code')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        by_status = (
            Student.objects.values('status')
            .annotate(count=Count('id'))
        )

        return Response({
            'total_students': total,
            'active_students': active,
            'average_gpa': round(avg_gpa, 2),
            'by_department': list(by_dept),
            'by_status': list(by_status),
        })
