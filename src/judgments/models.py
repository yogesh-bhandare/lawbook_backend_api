from django.db import models

class Judgment(models.Model):
    case_id = models.CharField(max_length=120, unique=True, db_index=True)
    url = models.URLField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)
    timestamp =  models.DateTimeField(auto_now_add=True)
    updated =  models.DateTimeField(auto_now=True)
    metadata = models.JSONField(null=True, blank=True)
    active = models.BooleanField(default=False, help_text="Scrape daily?")


class JudgmentScrapeEventManager(models.Manager):
    def create_scrape_event(self, json_data):
        events = [] 
        for obj in json_data:
            case_id = obj.get('WID') or None
            url = obj.get('link') or None
            content = obj.get('content') or None
            if case_id is None or url is None:
                continue

            # if content:
            #     content = "\n".join([line.strip() for line in content if line.strip()])
            # else:
            #     content = None
            
            judgment, _ = Judgment.objects.update_or_create(
                case_id=case_id,
                defaults={
                    "url": url,
                    "content": content,
                    "metadata": obj,
                }
            )
            event = self.create(
                judgment=judgment,
                url=url,
                case_id=case_id,
                data=obj,
            )
            events.append(event)  
        
        return events  


class JudgmentScrapeEvent(models.Model):
    judgment = models.ForeignKey(Judgment, on_delete=models.CASCADE, related_name='scrape_events')
    url = models.URLField(blank=True, null=True)
    data = models.JSONField(null=True, blank=True)
    case_id = models.CharField(max_length=120, null=True, blank=True)
    
    objects = JudgmentScrapeEventManager()
