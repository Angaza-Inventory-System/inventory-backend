import os
from haystack.query import SearchQuerySet
from rest_framework.response import Response
from rest_framework import mixins, generics, status
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'app_debug.log')

def log_to_file(message):
    """Helper function to write log messages to a file."""
    try:
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(message + '\n')
    except IOError as e:
        print(f"Error writing to log file: {e}")

class SearchAndLimitMixin:
    search_fields = []
    filterset_fields = []
    ordering_fields = []
    ordering = []

    def search_queryset(self, queryset, search_query):
        if search_query:
            sqs = SearchQuerySet().models(self.queryset.model).filter(content=search_query)
            for field in self.search_fields:
                sqs = sqs.filter(**{f"{field}__icontains": search_query})
            object_ids = [result.pk for result in sqs]
            pk_field = self.queryset.model._meta.pk.name
            queryset = queryset.filter(**{f"{pk_field}__in": object_ids})
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        limit = self.request.query_params.get('limit', None)

        queryset = self.search_queryset(queryset, search_query)
        
        if limit:
            queryset = queryset[:int(limit)]
        
        return queryset

class BatchCreateMixin(mixins.CreateModelMixin, generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        log_to_file(f"Received data: {data}")

        if data.get('batch') == True:
            # Batch creation
            nested_key = list(data.keys() - {'batch'})
            if len(nested_key) != 1:
                log_to_file(f"Invalid request format: {data}")
                return Response({"detail": "Request must contain exactly one nested key with a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

            nested_key = nested_key[0]
            objects_data = data[nested_key]
            log_to_file(f"Processing objects for key: {nested_key}")
            log_to_file(f"Objects data: {objects_data}")

            if isinstance(objects_data, list):
                created_objects = []
                errors = []

                for obj_data in objects_data:
                    try:
                        model_instance = self.queryset.model(**obj_data)
                        model_instance.save()
                        created_objects.append(model_instance.pk)
                        log_to_file(f"Created object with data: {obj_data}")
                    except IntegrityError as e:
                        log_to_file(f"IntegrityError for object data: {obj_data}, error: {e}")
                        errors.append({nested_key: str(e)})
                    except Exception as e:
                        log_to_file(f"Error for object data: {obj_data}, error: {e}")
                        errors.append({nested_key: str(e)})

                if errors:
                    log_to_file(f"Errors encountered: {errors}")
                    return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

                headers = self.get_success_headers(created_objects)
                return Response({"created_ids": created_objects}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                log_to_file(f"Invalid data format for key '{nested_key}': {objects_data}")
                return Response({"detail": f"Invalid data format. Expected a list of objects for key '{nested_key}'."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Single object creation
            return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save()
        log_to_file(f"Created object: {serializer.data}")

class BatchDeleteMixin(generics.GenericAPIView):
    def delete(self, request, *args, **kwargs):
        data = request.data
        log_to_file(f"Received data: {data}")

        if data.get('batch') == True:
            nested_key = list(data.keys() - {'batch'})
            if len(nested_key) != 1:
                log_to_file(f"Invalid request format: {data}")
                return Response({"detail": "Request must contain exactly one nested key with a list of IDs."}, status=status.HTTP_400_BAD_REQUEST)
            
            nested_key = nested_key[0]
            ids = data[nested_key]
            log_to_file(f"Processing IDs for key: {nested_key}")
            log_to_file(f"IDs data: {ids}")

            if isinstance(ids, list):
                queryset = self.get_queryset().filter(id__in=ids)
                count = queryset.count()
                
                try:
                    queryset.delete()
                    log_to_file(f"Deleted {count} items with IDs: {ids}")
                    return Response({"detail": f"Deleted {count} items."}, status=status.HTTP_204_NO_CONTENT)
                except IntegrityError as e:
                    log_to_file(f"IntegrityError during delete operation with IDs {ids}: {e}")
                    return Response({"detail": "Error occurred during delete operation."}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    log_to_file(f"Error during delete operation with IDs {ids}: {e}")
                    return Response({"detail": "Error occurred during delete operation."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                log_to_file(f"Invalid data format for key '{nested_key}': {ids}")
                return Response({"detail": f"Invalid data format. Expected a list of IDs for key '{nested_key}'."}, status=status.HTTP_400_BAD_REQUEST)
            
        else: 
            return super().delete(request, *args, **kwargs)
