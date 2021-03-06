# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.

from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

from caravaggio_rest_api.drf_haystack.serializers import BaseCachedSerializerMixin, CustomHaystackSerializer
from drf_haystack.serializers import HaystackFacetSerializer

from rest_framework import fields

from rest_framework_cache.registry import cache_registry

from caravaggio_rest_api.drf_haystack import serializers as dse_serializers

from davinci_crawling.example.bovespa.models import BovespaCompany, BovespaCompanyFile, BovespaAccount
from davinci_crawling.example.bovespa.search_indexes import (
    BovespaCompanyIndex,
    BovespaCompanyFileIndex,
    BovespaAccountIndex,
)


class BovespaCompanySerializerV1(dse_serializers.CassandraModelSerializer, BaseCachedSerializerMixin):
    """
    Represents a Business Object API View with support for JSON, list, and map
    fields.
    """

    class Meta:
        model = BovespaCompany
        fields = (
            "ccvm",
            "created_at",
            "cnpj",
            "updated_at",
            "company_name",
            "situation",
            "company_type",
            "is_deleted",
            "deleted_reason",
            "granted_date",
            "canceled_date",
        )

        read_only_fields = ("created_at", "updated_at")


class BovespaCompanySearchSerializerV1(CustomHaystackSerializer, BaseCachedSerializerMixin):
    """
    A Fast Searcher (Solr) version of the original Business Object API View
    """

    score = fields.FloatField(required=False)

    class Meta(CustomHaystackSerializer.Meta):
        model = BovespaCompany
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [BovespaCompanyIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "entity_type",
            "ccvm",
            "created_at",
            "cnpj",
            "updated_at",
            "company_name",
            "situation",
            "company_type",
            "granted_date",
            "canceled_date",
            "score",
        ]

        search_fields = ["text"]


class BovespaCompanyFacetSerializerV1(HaystackFacetSerializer):

    # Setting this to True will serialize the
    # queryset into an `objects` list. This
    # is useful if you need to display the faceted
    # results. Defaults to False.
    serialize_objects = True

    class Meta:
        index_classes = [BovespaCompany]
        fields = [
            "created_at",
            "updated_at",
            "situation",
            "company_type",
            "granted_date",
            "canceled_date",
            "ccvm",
            "cnpj",
        ]


# Cache configuration
cache_registry.register(BovespaCompanySerializerV1)
cache_registry.register(BovespaCompanySearchSerializerV1)


class BovespaCompanyFileSerializerV1(dse_serializers.CassandraModelSerializer, BaseCachedSerializerMixin):
    """
    Represents a Business Object API View with support for JSON, list, and map
    fields.
    """

    class Meta:
        model = BovespaCompanyFile
        fields = (
            "ccvm",
            "doc_type",
            "fiscal_date",
            "version",
            "status",
            "created_at",
            "updated_at",
            "protocol",
            "delivery_date",
            "delivery_type",
            "company_name",
            "company_cnpj",
            "fiscal_date_y",
            "fiscal_date_yd",
            "fiscal_date_q",
            "fiscal_date_m",
            "fiscal_date_md",
            "fiscal_date_w",
            "fiscal_date_wd",
            "fiscal_date_yq",
            "fiscal_date_ym",
            "source_url",
            "file_url",
            "file_name",
            "file_extension",
        )
        read_only_fields = ("created_at", "updated_at")


class BovespaCompanyFileSearchSerializerV1(CustomHaystackSerializer, BaseCachedSerializerMixin):
    """
    A Fast Searcher (Solr) version of the original Business Object API View
    """

    score = fields.FloatField(required=False)

    class Meta(CustomHaystackSerializer.Meta):
        model = BovespaCompanyFile
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [BovespaCompanyFileIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "ccvm",
            "doc_type",
            "fiscal_date",
            "version",
            "status",
            "created_at",
            "updated_at",
            "protocol",
            "delivery_date",
            "delivery_type",
            "company_name",
            "company_cnpj",
            "fiscal_date_y",
            "fiscal_date_yd",
            "fiscal_date_q",
            "fiscal_date_m",
            "fiscal_date_md",
            "fiscal_date_w",
            "fiscal_date_wd",
            "fiscal_date_yq",
            "fiscal_date_ym",
            "source_url",
            "file_url",
            "file_name",
            "file_extension",
            "score",
        ]

        search_fields = ["text"]


class BovespaCompanyFileFacetSerializerV1(HaystackFacetSerializer):

    # Setting this to True will serialize the
    # queryset into an `objects` list. This
    # is useful if you need to display the faceted
    # results. Defaults to False.
    serialize_objects = True

    class Meta:
        index_classes = [BovespaCompany]
        fields = [
            "ccvm",
            "doc_type",
            "fiscal_date",
            "version",
            "status",
            "created_at",
            "updated_at",
            "protocol",
            "delivery_date",
            "delivery_type",
            "company_name",
            "company_cnpj",
            "fiscal_date_y",
            "fiscal_date_yd",
            "fiscal_date_q",
            "fiscal_date_m",
            "fiscal_date_md",
            "fiscal_date_w",
            "fiscal_date_wd",
            "fiscal_date_yq",
            "fiscal_date_ym",
            "file_extension",
        ]


# Cache configuration
cache_registry.register(BovespaCompanyFileSerializerV1)
cache_registry.register(BovespaCompanyFileSearchSerializerV1)


class BovespaAccountSerializerV1(dse_serializers.CassandraModelSerializer, BaseCachedSerializerMixin):
    """
    Represents a Business Object API View with support for JSON, list, and map
    fields.
    """

    class Meta:
        model = BovespaAccount
        fields = (
            "ccvm",
            "period",
            "version",
            "number",
            "financial_info_type",
            "balance_type",
            "name",
            "amount",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class BovespaAccountSearchSerializerV1(CustomHaystackSerializer, BaseCachedSerializerMixin):
    """
    A Fast Searcher (Solr) version of the original Business Object API View
    """

    score = fields.FloatField(required=False)

    class Meta(CustomHaystackSerializer.Meta):
        model = BovespaAccount
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [BovespaAccountIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "ccvm",
            "period",
            "version",
            "number",
            "name",
            "financial_info_type",
            "balance_type",
            "comments",
            "amount",
            "created_at",
            "updated_at",
            "score",
        ]

        search_fields = ["text"]


class BovespaAccountFacetSerializerV1(HaystackFacetSerializer):

    # Setting this to True will serialize the
    # queryset into an `objects` list. This
    # is useful if you need to display the faceted
    # results. Defaults to False.
    serialize_objects = True

    class Meta:
        index_classes = [BovespaAccount]
        fields = [
            "ccvm",
            "period",
            "version",
            "number",
            "name",
            "financial_info_type",
            "balance_type",
            "comments",
            "created_at",
            "updated_at",
        ]


# Cache configuration
cache_registry.register(BovespaAccountSerializerV1)
cache_registry.register(BovespaAccountSearchSerializerV1)
