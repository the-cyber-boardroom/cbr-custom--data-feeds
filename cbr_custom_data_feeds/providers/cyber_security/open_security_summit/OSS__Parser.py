from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.models.Model__OSS__Page_Type       import Model__OSS__Page_Type
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.models.Model__OSS__Participant     import Model__OSS__Participant
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.models.Model__OSS__Working_Session import Model__OSS__Working_Session
from osbot_utils.base_classes.Type_Safe                                                                     import Type_Safe
from osbot_utils.utils.Misc                                                                                 import lower
from osbot_utils.utils.Objects                                                                              import obj


class OSS__Parser(Type_Safe):

    def parse_raw_content(self, raw_content):
        participants     = []
        working_sessions = []
        content          = dict(participants     = participants    ,
                                working_sessions = working_sessions)

        for item_raw in raw_content:
            item = obj(item_raw)
            page_type = Model__OSS__Page_Type(lower(item.type))
            if page_type == Model__OSS__Page_Type.PARTICIPANT:
                participant = self.parse_participant(item)
                participants.append(participant)
            elif page_type == Model__OSS__Page_Type.WORKING_SESSION:
                working_session = self.parse_working_session(item)
                working_sessions.append(working_session)
            # else:
            #    print('skiping page', item.title)
        return content

    def parse_participant(self, item) -> Model__OSS__Participant:    # Parse a participant entry
        website = item.website                                       # todo: refactor this 'fixing' logic
        if isinstance(website, str):                                 # support both strings and lists
            fixed__website = [website]
        else:
            fixed__website = website
        if item.linkedin:
            fixed__linkedin = item.linkedin.replace('https://www.linkedin.com/in/', '').replace('/', '')
        else:
            fixed__linkedin = ''

        return Model__OSS__Participant( title       = item.title             ,
                                        content     = item.content      ,
                                        description = item.description  ,
                                        type        = item.type         ,
                                        url         = item.url          ,
                                        permalink   = item.permalink    ,
                                        when_day    = item.when_day     ,
                                        when_month  = item.when_month   ,
                                        when_year   = item.when_year    ,
                                        when_time   = item.when_time    ,
                                        status      = item.status       ,
                                        company     = item.company      ,
                                        job_title   = item.job_title    ,
                                        linkedin    = fixed__linkedin   ,
                                        twitter     = item.twitter      ,
                                        facebook    = item.facebook     ,
                                        website     = fixed__website    ,
                                        image       = item.image        )
                 

    def parse_working_session(self, item) -> Model__OSS__Working_Session:    # Parse a working session entry
        organizers = item.organizers
        if isinstance(organizers, str):
            organizers = [org.strip() for org in organizers.split(',') if org.strip()]

        topics = item.topics
        if isinstance(topics, str):
            topics = [topic.strip() for topic in topics.split(',') if topic.strip()]

        return Model__OSS__Working_Session(
            title        = item.title       ,
            content      = item.content     ,
            description  = item.description ,
            type         = item.type        ,
            url          = item.url         ,
            permalink    = item.permalink   ,
            when_day     = item.when_day    ,
            when_month   = item.when_month  ,
            when_year    = item.when_year   ,
            when_time    = item.when_time   ,
            status       = item.status      ,
            event        = item.event       ,
            organizers   = organizers       ,
            topics       = topics           ,
            track        = item.track       ,
            youtube_link = item.youtube_link,
            zoom_link    = item.zoom_link   ,
            hey_summit   = item.hey_summit  )