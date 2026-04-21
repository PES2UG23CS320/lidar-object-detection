import numpy as np

MAX_DISTANCE = 1.0   # increased tolerance
MAX_MISSED = 3      # memory for lost objects

class Tracker:
    def __init__(self):
        self.objects = []
        self.next_id = 0

    def update(self, clusters):
        new_objects = []

        # Match clusters to existing objects
        for cluster in clusters:
            if len(cluster) == 0:
                continue

            center = np.mean(cluster, axis=0)

            # Safety check
            if not isinstance(center, (list, tuple, np.ndarray)):
                continue
            if len(center) < 2:
                continue

            matched = None
            min_dist = float('inf')

            # Find closest object
            for obj in self.objects:
                dist = np.linalg.norm(center - obj['position'])
                if dist < MAX_DISTANCE and dist < min_dist:
                    matched = obj
                    min_dist = dist

            if matched:
                # smoothing to reduce jitter
                alpha = 0.7
                new_pos = alpha * matched['position'] + (1 - alpha) * center

                velocity = np.linalg.norm(new_pos - matched['position'])

                matched['position'] = new_pos
                matched['velocity'] = velocity
                matched['missed'] = 0

                new_objects.append(matched)

            else:
                # New object
                new_objects.append({
                    'id': self.next_id,
                    'position': center,
                    'velocity': 0.0,
                    'missed': 0
                })
                self.next_id += 1

        # Keep unmatched objects for few frames
        for obj in self.objects:
            if obj not in new_objects:
                obj['missed'] += 1
                if obj['missed'] < MAX_MISSED:
                    new_objects.append(obj)

        self.objects = new_objects
        return self.objects
