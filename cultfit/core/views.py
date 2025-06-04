from django.shortcuts import render
from .models import FitnessClass
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email, validate_integer
from django.core.exceptions import ValidationError


# Returns a list of all upcoming fitness classes 
# (name, date/time, instructor, available slots)

class AllClassesView(APIView):
    # GET request to return all classes
    def get(self, request):
        all_classes = FitnessClass.objects.all()
        # Filter out classes with no available slots
        for fitness_class in all_classes:
            # Check if the class has registered clients
            if fitness_class.total_slots <= 0:
                # Exclude classes with no available slots
                all_classes = all_classes.exclude(id=fitness_class.id)        
        return Response(all_classes.values(), status=status.HTTP_200_OK)

# Accepts a booking request (class_id, client_name, client_email)
# Validates if slots are available, and reduces available slots upon successful booking
    
class BookClassView(APIView):
    # POST request to book a class
    def post(self, request):
        # required fields: class_id, client_name, client_email to book a class
        class_id = request.data.get('class_id')
        client_name = request.data.get('client_name')
        client_email = request.data.get('client_email')
        
        try:
            # Validate the email format
            validate_email(client_email)
        except ValidationError:
            return Response({"message": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if all required fields are provided
        if not all([class_id, client_name, client_email]):
            return Response({"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the class_id is provided
        if not class_id:
            return Response({"message": "Class ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the client_name is provided
        if not client_name:
            return Response({"message": "Client name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_integer(class_id)
        except ValidationError:
            return Response({"message": "Invalid class ID format"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Fetch the fitness class by ID
            fitness_class = FitnessClass.objects.get(id=class_id)
            # Check if the client is already registered for the class
            if fitness_class.registered_clients is not None:
                if client_email in fitness_class.registered_clients:
                    return Response({"message": "Client already registered"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Initialize registered_clients if it is None
                fitness_class.registered_clients = []
            # Check if there are available slots
            if fitness_class.total_slots > 0:
                # If slots are available, register the client
                if fitness_class.registered_clients is not None:
                    fitness_class.registered_clients.append(client_email)
                else:
                    fitness_class.registered_clients = [client_email]
                fitness_class.total_slots -= 1
                fitness_class.save()
                return Response({"message": "Client registered successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No slots available"}, status=status.HTTP_400_BAD_REQUEST)
        # If the class does not exist, return a 404 error
        except FitnessClass.DoesNotExist:
            return Response({"message": "Class not found"}, status=status.HTTP_404_NOT_FOUND)




# Returns all bookings made by a specific email address

class ClassesByClientView(APIView):
    # GET request to return all classes booked by a specific client
    def get(self, request, email_id):
        
        try:
            # Validate the email format
            validate_email(email_id)
        except ValidationError:
            return Response({"message": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Fetch all fitness classes
            classes = FitnessClass.objects.all()
            client_classes = []
            for fitness_class in classes:
                # Check if the client is registered for the class
                if email_id in list(fitness_class.registered_clients):
                    # If registered, add the class name to the list
                    client_classes.append(fitness_class.name)
            if not client_classes:
                return Response({"message": "No classes found for this client"}, status=status.HTTP_404_NOT_FOUND)
            # Return the list of classes registered by the client
            return Response(client_classes, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle any exceptions and return a 400 error
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

