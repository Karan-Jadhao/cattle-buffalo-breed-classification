import { useTranslation } from "react-i18next";
import {
  Image,
  UserRound,
  Sun,
  ScanFace
} from "lucide-react";

import "./SupportedImages.css";

function SupportedImages() {
  const { t } = useTranslation();

  const items = [
    {
      icon: Image,
      title: t("supportedImages.item1Title"),
      description: t("supportedImages.item1Desc")
    },
    {
      icon: UserRound,
      title: t("supportedImages.item2Title"),
      description: t("supportedImages.item2Desc")
    },
    {
      icon: Sun,
      title: t("supportedImages.item3Title"),
      description: t("supportedImages.item3Desc")
    },
    {
      icon: ScanFace,
      title: t("supportedImages.item4Title"),
      description: t("supportedImages.item4Desc")
    }
  ];

  return (
    <section className="supported-images">

      <div className="supported-heading">
        <strong>{t("supportedImages.title")}</strong>
        <span>{t("supportedImages.specs")}</span>
      </div>

      {items.map((item) => {

        const Icon = item.icon;

        return (
          <div className="supported-item" key={item.title}>

            <div className="supported-icon">
              <Icon size={19} />
            </div>

            <div>
              <strong>{item.title}</strong>
              <p>{item.description}</p>
            </div>

          </div>
        );
      })}

    </section>
  );
}

export default SupportedImages;