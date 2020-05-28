
class Utils:

    def limitQueryset(self, queryset, start_limit, end_limit):
        # limits the total response count        
        if start_limit and end_limit: # case1: both are present
            queryset = queryset[int(start_limit)-1:int(end_limit)]
        elif start_limit: # case2: only start_limit is present
            queryset = queryset[int(start_limit)-1:]
        elif end_limit: # case3: only end_limit is present
            queryset = queryset[:int(end_limit)]

        return queryset

