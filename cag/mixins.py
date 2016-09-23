#coding=utf-8

class AgenciaMixin(object):

    def get_queryset(self, **kwargs):
        empresa = self.request.user.profile.empresa_id
        bsr = self.request.user.profile.baseregional_id
        reg = self.request.user.profile.regional_id
        if reg is not None and bsr is not None:
            return super(AgenciaMixin, self).get_queryset() \
                .select_related('regional') \
                .select_related('baseregional') \
                .select_related('empresa') \
                .filter(empresa=empresa, regional=reg, baseregional=bsr)
        elif reg is not None and bsr is None:
            return super(AgenciaMixin, self).get_queryset() \
                .select_related('regional') \
                .select_related('baseregional') \
                .select_related('empresa') \
                .filter(empresa=empresa, regional=reg)
        elif reg is None and bsr is not None:
            return super(AgenciaMixin, self).get_queryset() \
                .select_related('regional') \
                .select_related('baseregional') \
                .select_related('empresa') \
                .filter(empresa=empresa, baseregional=bsr)
        else:
            return super(AgenciaMixin, self).get_queryset() \
                .select_related('regional') \
                .select_related('baseregional') \
                .select_related('empresa') \
                .filter(empresa=empresa)
