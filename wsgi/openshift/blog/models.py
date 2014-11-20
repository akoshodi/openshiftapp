from django.db import models

# Create your models here.


from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel ,MultiFieldPanel,InlinePanel, PageChooserPanel
from modelcluster.fields import ParentalKey


from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase



class LinkFields(models.Model):
	link_page = models.ForeignKey(
		'wagtailcore.Page',
		null=True,
		blank=True,
		related_name='+'
	)

	panels = [
		PageChooserPanel('link_page'),
	]
	class Meta:
		abstract = True

class RelatedLink(LinkFields):
	title = models.CharField(max_length=255, help_text="Link title")
	panels = [
	FieldPanel('title'),
	MultiFieldPanel(LinkFields.panels, "Link"),
]

class Meta:
	abstract = True



class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPage', related_name='tagged_items')  
class BlogPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('blog.BlogPage', related_name='related_links')

class BlogPage(Page):
	intro = RichTextField(blank=True)
	body = RichTextField()
	tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
	date = models.DateField("Post date")
	search_name = "Blog Page"
	indexed_fields = ('body', )

BlogPage.content_panels = [
	FieldPanel('title', classname="full title"),
	FieldPanel('date'),
	FieldPanel('intro', classname="full"),
	FieldPanel('body', classname="full"),
	InlinePanel(BlogPage, 'related_links', label="Related links"),
]




class BlogIndexPageRelatedLink(Orderable, RelatedLink):
	page = ParentalKey('blog.BlogIndexPage', related_name='related_links')

class BlogIndexPage(Page):
	intro = models.CharField(max_length=256)
	indexed_fields = ('body', )
	search_name = "Blog Index Page"

BlogIndexPage.content_panels = [
	FieldPanel('title', classname="full title"),
	FieldPanel('intro', classname="full"),
	InlinePanel(BlogIndexPage, 'related_links', label="Related links"),
]